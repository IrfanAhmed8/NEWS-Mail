import requests
from bs4 import BeautifulSoup

url = "https://www.aljazeera.com/"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Try multiple possible article title classes
all_links = []

# Option 1: Liveblog articles
liveblogs = soup.find_all('div', class_='article-card__liveblog-title')
for lb in liveblogs:
    a_tag = lb.find('a')
    if a_tag:
        title = a_tag.get_text(strip=True)
        link = a_tag['href']
        if not link.startswith("http"):
            link = "https://www.aljazeera.com" + link
        all_links.append((title, link))



# Option 2: Regular article cards
regulars = soup.find_all('a', class_='u-clickable-card__link')
for reg in regulars:
    title = reg.get_text(strip=True)
    link = reg['href']
    if not link.startswith("http"):
        link = "https://www.aljazeera.com" + link
    all_links.append((title, link))




# Remove duplicates and print top 10
unique_links = []
seen = set()

for title, link in all_links:
    if link not in seen and title:
        seen.add(link)
        unique_links.append((title, link))
    if len(unique_links) == 10:
        break

# Show results
for i, (title, link) in enumerate(unique_links, start=1):
    print(f"{i}. {title}\n   {link}")
