import requests
from bs4 import BeautifulSoup
import time
from BBCdb import BBC,db

from summarizer import summarize_paragraphs

class AlJazeeraScraper:
    def __init__(self, base_url):
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
    #function called in collect_links
    #used for making link for the title
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
            text = ' '.join(p.get_text(strip=True) for p in paragraphs)  # Join all paragraphs into one string
            image_div = soup.find('div', class_='responsive-image')
            
            if image_div:
                img_tag = image_div.find('img')
                if img_tag and img_tag.has_attr('src'):
                    img_src = img_tag['src']
                    if img_src.startswith('/'):
                        # relative path: prepend domain
                        image = self.base_url + img_src
                    else:
                        image = img_src

            return text, image
        except Exception as e:
            print("Error fetching article:", e)
            return '', ''
    def copy_all_to_BBC_db(self):
        for article_data in self.unique_links:
            existing = BBC.query.filter_by(title=article_data['Title']).first()
            print("adding data to sql")
            if  not  existing:
                bbc_data=BBC(title=article_data['Title'],
                            link=article_data['Link'],
                            content=article_data['Content'],
                            image=article_data['Image'],
                            summary=article_data['summary']
                            )
                db.session.add(bbc_data)
                db.session.commit()
            else:
                print(f"{article_data['Title']} skipped")

    #delete all row from the BBC table           
    def Delete_row_BBC(self):
        if db.session.query(BBC).count() > 0:
            db.session.query(BBC).delete()
            db.session.commit()
            print("cleaned all the rows and storing 10 new headlines")
        

    def summarize_paragraph(self):
        for link in self.unique_links:
            paragraph = link['Content']
            summary = summarize_paragraphs(paragraph)
            link['summary'] = summary

    def add_content_image(self):
        for item in self.unique_links:
            
            content, image = self.get_info_and_image(item["Link"])
            item["Content"] = content
            item["Image"] = image
    
    #combine all and add all data to the sqllite             
    def scrape(self):
        soup = self.fetch_homepage()
        all_links = self.collect_links(soup)
        self.remove_duplicates_and_limit(all_links)
        self.add_content_image()
        self.summarize_paragraph()
        self.Delete_row_BBC()
        self.copy_all_to_BBC_db()






