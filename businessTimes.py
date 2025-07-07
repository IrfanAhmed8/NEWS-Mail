import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from BBCdb import db,businessDB
from summarizer import summarize_paragraphs


class businessScrapper:
    def __init__(self, url):
        self.url = url
        self.link_List = []

    def fetch_homepage(self):
        response = requests.get(self.url)
        return BeautifulSoup(response.text, "html.parser")

    from urllib.parse import urljoin

    def collect_link(self, soup):
        try:
            # Look for divs with the correct class
            list_items = soup.find_all('div', class_="lst_li_rhs")
            
            for item in list_items:
                title_link = item.find('a', class_="lst_lnk_txt")
                
                if title_link and 'href' in title_link.attrs:
                    title = title_link.get('title', title_link.get_text(strip=True))
                    full_link = title_link['href']
                    
                    if not full_link.startswith("http"):
                        full_link = urljoin(self.url, full_link)
                    
                    self.link_List.append({'Title': title, 'Link': full_link})
                    print({'Title': title, 'Link': full_link})

        except Exception as e:
            print("Issue in scraping:", e)

        finally:
            print("link_List is filled")
            return self.link_List

        
    def collect_info_for_link(self):
        for link in self.link_List:
            try:
                print(f"Fetching content and image from: {link['Link']}")
                response = requests.get(link['Link'])
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract content
                container = soup.find('div', class_="story_witha_main_sec")
                paragraphs = container.find_all('p') if container else []
                text = ' '.join(p.get_text(strip=True) for p in paragraphs)
                link['Content'] = text

                # Extract image
                image_container = soup.find('div', class_="main_img")
                image_tag = image_container.find('img') if image_container else None
                image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else ''
                link['Image'] = image_url
                print(f"Info--{link['Content']} \n  Image--{link['Image']}")
            except Exception as e:
                print(f"Error fetching article from {link['Link']}: {e}")
                link['Content'] = ''
                link['Image'] = ''


    def copy_to_businessDB(self):
        for link_data in self.link_List:
            existing = businessDB.query.filter_by(title=link_data['Title']).first()
            print("Adding data to SQL")
            if not existing:
                business_data = businessDB(
                    title=link_data['Title'],
                    link=link_data['Link'],
                    content=link_data.get('Content', ''),
                    image=link_data.get('Image', '')
                )
                db.session.add(business_data)
                db.session.commit()
            else:
                print(f"{link_data['Title']} already exists, skipping.")

    def summarize_content(self):
        for item in self.link_List:
            content = item.get('Content', '')
            summary = summarize_paragraphs(content)
            item['Summary'] = summary
            print(f"{summary}")

    def Delete_row_Business(self):
        if db.session.query(businessDB).count() > 0:
            db.session.query(businessDB).delete()
            db.session.commit()
            print("cleaned all the rows and storing 10 new headlines")
   
    def scrape(self):
        print("Fetching homepage...")
        soup = self.fetch_homepage()

        print("Collecting article links...")
        self.collect_link(soup)

        print("Extracting content and images from articles...")
        self.collect_info_for_link()

        self.summarize_content()
        self.Delete_row_Business()
        print("Storing data into the database...")
        self.copy_to_businessDB()

        print("Scraping complete!")




