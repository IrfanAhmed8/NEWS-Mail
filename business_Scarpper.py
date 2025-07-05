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

    def collect_link(self, soup):
        try:
            links = soup.find_all('span', class_="line-clamp-3")
            for item in links:
                title = item.get_text(strip=True)
                a_tag = item.find_parent('a')
                if a_tag and 'href' in a_tag.attrs:
                    full_link = a_tag['href']
                    if not full_link.startswith("http"):
                        full_link = urljoin(self.url, full_link)
                    self.link_List.append({'Title': title, 'Link': full_link})
        except Exception as e:
            print("Issue in scraping:", e)
        finally:
            print("link_List is filled")
            return self.link_List

    def collect_info_for_link(self):
        for link in self.link_List:
            try:
                response = requests.get(link['Link'])
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract content
                container = soup.find(
                    'div',
                    class_="mx-auto mb-4 break-words font-merriweatherSans text-base font-base-normal leading-[1.75] lg:text-lg"
                )
                paragraphs = container.find_all('p') if container else []
                text = ' '.join(p.get_text(strip=True) for p in paragraphs)
                link['Content'] = text

                # Extract image
                img_tag = soup.find('img', src=lambda s: s and 'cassette.sphdigital.com.sg' in s)
                if img_tag and img_tag.has_attr('src'):
                    img_src = img_tag['src']
                    image = urljoin(self.url, img_src) if img_src.startswith('/') else img_src
                    link['Image'] = image
                else:
                    link['Image'] = ''
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

   
    def scrape(self):
        print("Fetching homepage...")
        soup = self.fetch_homepage()

        print("Collecting article links...")
        self.collect_link(soup)

        print("Extracting content and images from articles...")
        self.collect_info_for_link()

        self.summarize_content()

        print("Storing data into the database...")
        self.copy_to_businessDB()

        print("Scraping complete!")
