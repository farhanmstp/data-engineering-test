# Technical Test - Data Engineering

Project ini merupakan implementasi web crawler dan article scraper untuk situs Bisnis.com.
Crawler mendukung dua mode pengambilan data:

- Backtrack Mode → mengambil artikel lama dalam rentang tanggal tertentu
- Standard Mode → mengambil artikel terbaru secara periodik (real-time)

## Arsitektur Project

TestDataEngineering/
│
├── core/
│   ├── scraper.py       → Fungsi untuk scrape satu artikel tunggal
│   └── crawler.py       → Fungsi discover_links (ambil link dari index page)
│                        → Fungsi crawl_articles (scrape banyak artikel)
│
├── test/                → Unit test/manual testing script
│   ├── test_scraper.py
│   ├── test_crawler.py
│   └── test_crawlr_articles.py
│
├── backtrack.py         → Mode historical crawling (ambil artikel lama)
├── standard.py          → Mode real-time crawling (ambil artikel terbaru)
└── README.md

Penjelasan arsitektur

- scraper.py
  Mengambil:
    - title
    - publish date (dinormalisasi ISO format)
    - content
    - url

- crawler.py
  - discover_links() → Mengambil daftar URL artikel dari halaman kategori
  - crawl_articles() → Menjalankan scraper untuk banyak artikel sekaligus

- backtrack.py
  Looping halaman ke belakang sampai menemukan artikel dalam rentang tanggal
  lalu berhenti otomatis saat tanggal artikel < start date.

- standard.py
  Loop infinite (sampai dihentikan) untuk mengambil artikel baru dari page 1
  setiap X detik, hanya menyimpan artikel yang belum pernah diambil (anti-duplikasi).

## Fungsi Dasar Crawler

1. Discover Links
  Mengambil seluruh link artikel dari halaman kategori, contoh:

  https://www.bisnis.com/index?categoryId=186&page=1


  Fungsi:

  discover_links(base_url, page_number)

2. Crawl Articles
  Menjalankan scraper pada seluruh link yang ditemukan:

  crawl_articles(list_of_urls)

3. Scraper
  Mengambil:
  - title
  - publish_date (ISO)
  - content
  - url
  dari satu halaman artikel.

4. Backtrack Logic
  - Loop halaman 1, 2, 3, dst
  - scrape artikel
  - hentikan jika publish_date < start_date
  - hanya simpan artikel dalam interval start–end

5. Standard Logic
  - Ambil link terbaru dari page 1
  - cek apakah ada artikel baru (belum tercatat di JSON)
  - scrape hanya artikel baru
  - simpan
  - tunggu interval
  - ulangi

## Backtrack Mode (Historical Crawling)

Menjalankan crawler untuk mengambil artikel dalam rentang tanggal tertentu:

python backtrack.py --category market --start 2025-11-01 --end 2025-11-15 --output hasil_backtrack.json


Output berupa JSON:

[
  {
    "url": "...",
    "title": "...",
    "publish_date": "2025-11-02T10:00:00+07:00",
    "content": "..."
  }
]

## Standard Mode (Real-Time Crawling)

Menjalankan crawler untuk mengambil artikel baru setiap interval X detik:

python standard.py --category market --interval 60 --output realtime.json

Contoh output terminal:

-----
Crawling kategori: market
Menemukan 3 artikel baru.
Menyimpan 3 artikel baru ke realtime.json
Tidur 60 detik ...
-----
Tidak ada artikel baru.
Tidur 60 detik ...

Mode ini berjalan terus sampai dihentikan dengan CTRL + C.