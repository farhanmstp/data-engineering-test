import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.crawler import discover_links

CATEGORY = "https://www.bisnis.com/index?categoryId=186"  # kabar24

links = discover_links(CATEGORY, 1)

print("Jumlah link:", len(links))
for l in links[:5]:
    print(l)