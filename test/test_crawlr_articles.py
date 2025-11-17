import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.crawler import discover_links, crawl_articles

CATEGORY = "https://www.bisnis.com/index?categoryId=186"

links = discover_links(CATEGORY, 1)
print("Jumlah link =", len(links))

articles = crawl_articles(links[:3])   # ambil 3 dulu supaya cepat
print("Jumlah artikel berhasil =", len(articles))

for art in articles:
    print(art["title"])
    print(art["publish_date"])
    print(art["content"][:300])
    print("-----------")