import requests
from bs4 import BeautifulSoup

def dynamic_scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    data = {}

    # Generic scraping logic
    # For titles
    titles = soup.find_all(['h1', 'h2', 'h3'])
    data['titles'] = [title.get_text(strip=True) for title in titles if title]

    # For paragraphs (bio, descriptions)
    paragraphs = soup.find_all('p')
    data['paragraphs'] = [para.get_text(strip=True) for para in paragraphs if para]

    # Extract images
    images = soup.find_all('img', src=True)
    data['images'] = [img['src'] for img in images if img['src'].startswith('http')]

    return data
