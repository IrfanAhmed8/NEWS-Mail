import requests
from bs4 import BeautifulSoup
import time
from BBCdb import BBC,db
class AlJazeeraScraper:
    def __init__(self, base_url="https://www.aljazeera.com/"):
        self.base_url = base_url
        self.unique_links = []

    def fetch_homepage(self):
        response = requests.get(self.base_url)
        return BeautifulSoup(response.text, 'html.parser')

    def collect_links(self, soup):
        all_links = []

        # Liveblog articles
        liveblogs = soup.find_all('div', class_='article-card__liveblog-title')
        for lb in liveblogs:
            a_tag = lb.find('a')
            if a_tag:
                title = a_tag.get_text(strip=True)
                link = self.full_url(a_tag['href'])
                all_links.append((title, link))

        # Regular article cards
        regulars = soup.find_all('a', class_='u-clickable-card__link')
        for reg in regulars:
            title = reg.get_text(strip=True)
            link = self.full_url(reg['href'])
            all_links.append((title, link))

        return all_links

    def full_url(self, link):
        return link if link.startswith("http") else self.base_url.rstrip("/") + link

    def remove_duplicates_and_limit(self, all_links, limit=10):
        seen = set()
        for title, link in all_links:
            if link not in seen and title:
                seen.add(link)
                self.unique_links.append({"Title": title, "Link": link})
            if len(self.unique_links) == limit:
                break

    def get_info_and_image(self, link):
        print("Fetching info from:", link)
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')

            container = soup.find('div', class_='wysiwyg wysiwyg--all-content')
            paragraphs = container.find_all('p') if container else []
            image_div = soup.find('div', class_='responsive-image')
            image=''
            if image_div:
                img_tag = image_div.find('img')
                if img_tag and img_tag.has_attr('src'):
                    image = img_tag['src']
            text = ' '.join(p.get_text(strip=True) for p in paragraphs)
            return text, image
        except Exception as e:
            print("Error fetching content:", e)
            return None, None

    def scrape(self):
        soup = self.fetch_homepage()
        all_links = self.collect_links(soup)
        self.remove_duplicates_and_limit(all_links)

        for item in self.unique_links:
            
            content, image = self.get_info_and_image(item["Link"])
            item["Content"] = content
            item["Image"] = image

    def show_results(self):
        for item in self.unique_links:
            print(f"Title: {item['Title']}")
            print(f"Link: {item['Link']}")
            print(f"Content: {item['Content'][:200]}...")
            print(f"ImageLink: {item['Image']}")
            print("\n")

    def copy_all_to_BBC_db(self):
        for article_data in self.unique_links:
            print("adding data to sql")
            bbc_data=BBC(title=article_data['Title'],
                         link=article_data['Link'],
                         content=article_data['Content'],
                         image=article_data['Image']
                         )
            db.session.add(bbc_data)
            db.session.commit()
            


# === Run the Scraper ===
if __name__=="__main__":
        from app import app
        scraper = AlJazeeraScraper()
        scraper.scrape()
        
        with app.app_context():  # <-- Ensure Flask app context is active
            scraper.copy_all_to_BBC_db()

       # scraper.show_results()
       # print("\nSleeping for 1 hour...\n")
       # time.sleep(60*60)
