import requests
from bs4 import BeautifulSoup
from core.scraper import scrape_article

def discover_links(category_base_url, page_number):
    # Membangun URL halaman listing
    url = f"{category_base_url}&page={page_number}"

    # Meminta HTML dari website
    response = requests.get(url)
    response.raise_for_status()
    html = response.text

    # Parsing
    soup = BeautifulSoup(html, "lxml")

    # Menemukan link artikel
    article_blocks = soup.find_all("div", class_="art--row")

    links = []
    for block in article_blocks:
        a_tag = block.find("a", href=True)
        if a_tag:
            href = a_tag["href"]
            links.append(href)

    return links

def crawl_articles(url_list):
    results = []

    # looping untuk setiap URL
    for url in url_list:
        try:
            article = scrape_article(url)
            results.append(article)
        except Exception as e:
            print(f"Gagal scrape {url}: {e}")
            continue

    return results