from scraper.scraper import scrape_prothomalo
from scraper.csv_writer import save_to_csv
from scraper.config import CSV_FILE_PATH


def main():
    print("▶ Scraping Prothom Alo via RSS")

    data = scrape_prothomalo()

    if data:
        save_to_csv(data, CSV_FILE_PATH)
        print(f"[✔] Total articles scraped: {len(data)}")
    else:
        print("⚠ No data found")


if __name__ == "__main__":
    main()
