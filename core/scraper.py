import requests
from bs4 import BeautifulSoup
from dateutil import parser

def scrape_article(url):
    # Meminta HTML dari website
    response = requests.get(url)
    response.raise_for_status()
    html = response.text

    # Parsing
    soup = BeautifulSoup(html,"lxml")

    # Mencari title
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else ""

    # Mencari tanggal publish
    published_at = ""
    time_tag = soup.find("time")
    if time_tag and time_tag.has_attr("datetime"):
        published_at = time_tag["datetime"]
    else:
        meta_time = soup.find("meta", {"property": "article:published_time"})
        if meta_time and meta_time.get("content"):
            published_at = meta_time["content"]

    # Normalisasi tanggal ke format ISO 8601
    if published_at:
        try:
            dt = parser.parse(published_at)
            published_at = dt.isoformat()
        except:
            pass

    # Mencari isi konten
    content = ""
    container = soup.find("article", class_="detailsContent")

    if container:
        paragraphs = container.find_all("p")
        content = "\n".join(
            p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)
        )

    # Return semua nilai yang dicari
    return {
        "url": url,
        "title": title,
        "publish_date": published_at,
        "content": content
    }