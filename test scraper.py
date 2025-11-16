from core.scraper import scrape_article

url = "https://ekonomi.bisnis.com/read/20251116/10/1929201/pembangunan-kopdes-merah-putih-dari-apbn-purbaya-bakal-cicil-rp240-triliun-ke-himbara"
data = scrape_article(url)

print(data["title"])
print(data["publish_date"])
print(data["content"][:500])
