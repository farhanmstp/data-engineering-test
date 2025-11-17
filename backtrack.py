import argparse
from dateutil import parser
from core.crawler import discover_links, crawl_articles
from datetime import timezone, timedelta
import json

CATEGORY_MAP = {
    "market": "https://www.bisnis.com/index?categoryId=194"
}

def parse_args():
    parser = argparse.ArgumentParser(description="Backtrack news articles")

    parser.add_argument("--category", required=True, help="Kategori, contoh: kabar24")
    parser.add_argument("--start", required=True, help="Tanggal awal (YYYY-MM-DD)")
    parser.add_argument("--end", required=True, help="Tanggal akhir (YYYY-MM-DD)")
    parser.add_argument("--output", default="backtrack_output.json", help="File output JSON")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    category = args.category.lower()

    # Memastikan category sesuai pilihan
    if category not in CATEGORY_MAP:
        print("Kategori tidak dikenal. Pilih salah satu:", ", ".join(CATEGORY_MAP.keys()))
        exit()

    category_base_url = CATEGORY_MAP[category]

    # Parse tanggal
    start_date = parser.parse(args.start)
    end_date = parser.parse(args.end)

    # Tambahkan timezone Waktu Indonesia Barat (+07:00)
    WIB = timezone(timedelta(hours=7))
    start_date = start_date.replace(tzinfo=WIB)
    end_date = end_date.replace(tzinfo=WIB)

    print("Base URL category:", category_base_url)
    print("Start date (parsed):", start_date)
    print("End date (parsed):", end_date)

    # Loop backtrack 
    results = []
    page = 1
    stop = False

    while not stop:
        print(f"Processing page {page} ...")

        links = discover_links(category_base_url, page)
        if not links:
            print("Tidak ada link lagi, berhenti.")
            break

        articles = crawl_articles(links)

        for art in articles:
            pub_date = parser.parse(art["publish_date"])

            # kalau sudah melewati tanggal start, stop total
            if pub_date < start_date:
                stop = True
                break

            # simpan hanya artikel yang dalam rentang
            if start_date <= pub_date <= end_date:
                results.append(art)

        page += 1

# Save to JSON
with open(args.output, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Saved {len(results)} articles to {args.output}")