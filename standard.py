import argparse
import time
import json
import os
from core.crawler import discover_links, crawl_articles

CATEGORY_MAP = {
    "market": "https://www.bisnis.com/index?categoryId=194",
    "kabar24": "https://www.bisnis.com/index?categoryId=186"
}

def parse_args():
    parser = argparse.ArgumentParser(description="Standard crawling mode")

    parser.add_argument(
        "--category",
        required=True,
        help="Kategori yang ingin dicrawl, misal 'market' atau 'kabar24'"
    )

    parser.add_argument(
        "--interval",
        default=60,
        type=int,
        help="Interval (detik) antar crawling. Default 60 detik."
    )

    parser.add_argument(
        "--output",
        default="standard_output.json",
        help="File output JSON"
    )

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    # Validasi kategori
    category = args.category.lower()
    if category not in CATEGORY_MAP:
        print("Kategori tidak dikenal. Pilih salah satu:", ", ".join(CATEGORY_MAP.keys()))
        exit()

    category_base_url = CATEGORY_MAP[category]

    # Load data yang sudah ada
    if os.path.exists(args.output):
        with open(args.output, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_urls = {article["url"] for article in existing_data}

    # Looping utama
    while True:
        print("-----")
        print("Crawling kategori:", category)
        print("Mengambil data dari:", category_base_url)

        # Ambil link terbaru dari halaman 1
        links = discover_links(category_base_url, 1)

        # Filter link yang belum pernah disimpan
        new_links = [url for url in links if url not in existing_urls]

        if not new_links:
            print("Tidak ada artikel baru.")
        else:
            print(f"Menemukan {len(new_links)} artikel baru.")

            # Scrape artikel baru saja
            new_articles = crawl_articles(new_links)

            # Tambah ke data existing
            existing_data.extend(new_articles)

            # Update URL set
            for art in new_articles:
                existing_urls.add(art["url"])

            # Simpan kembali JSON
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)

            print(f"Menyimpan {len(new_articles)} artikel baru ke {args.output}")

        print(f"Tidur {args.interval} detik ...")
        time.sleep(args.interval)