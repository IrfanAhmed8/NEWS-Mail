import requests
from bs4 import BeautifulSoup
# link for al jazeera       
url = "https://www.aljazeera.com/"
unique_links = []

#Fetch html content from the URL
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Try multiple possible article title classes
all_links = []

# Liveblog articles
def collect_links(soup):
    liveblogs = soup.find_all('div', class_='article-card__liveblog-title')
    for lb in liveblogs:
        a_tag = lb.find('a')
        if a_tag:
            title = a_tag.get_text(strip=True)
            link = a_tag['href']
            if not link.startswith("http"):
                link = "https://www.aljazeera.com" + link
            all_links.append((title, link))



    # Regular article cards

    regulars = soup.find_all('a', class_='u-clickable-card__link')
    for reg in regulars:
        title = reg.get_text(strip=True)
        link = reg['href']
        if not link.startswith("http"):
            link = "https://www.aljazeera.com" + link
        all_links.append((title, link))




# Remove duplicates and print top 10
def remove_duplicates_and_limit(all_links):
    
    seen = set()

    for title, link in all_links:
        if link not in seen and title:
            seen.add(link)
            unique_links.append({"Title":title,"Link": link})
        if len(unique_links) == 10:
            break
   


def get_info(link):
    print("Fetching information from:", link)
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')

        container = soup.find('div', class_='wysiwyg wysiwyg--all-content')
        paragraphs=container.find_all('p')
        # Extract text from all paragraphs and join them
        text = ' '.join(p.get_text(strip=True) for p in paragraphs)
        return text

    except Exception as e:
        print("Didn't able to print the paragraph. Error:", e)
        return None



# Show results

def show_info_about_link():
    collect_links(soup)
    remove_duplicates_and_limit(all_links)
    print("Top 10 unique links:")
    for item in unique_links:
        link= item['Link']
        result=get_info(link)
        item['Content'] = result

show_info_about_link()
for item in unique_links:
    print(f"Title: {item['Title']}")
    print(f"Link: {item['Link']}")
    print(f"Content: {item['Content'][:200]}...")  
    print("\n")
    








