import csv
from dataclasses import dataclass
from typing import List, Tuple
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

@dataclass
class Source:
    name: str
    url: str
    item_selector: str  # CSS селектор элементов ссылок заголовков

SOURCES = [
    Source(name="Lenta", url="https://lenta.ru/", item_selector="a.card-mini__title"),
    Source(name="Habr", url="https://habr.com/ru/all/", item_selector="article a.tm-title__link"),
]

def fetch(source: Source) -> List[Tuple[str, str]]:
    r = requests.get(source.url, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    items = soup.select(source.item_selector)
    results = []
    for a in items:
        title = a.get_text(strip=True)
        href = a.get("href")
        if href and href.startswith('/'):
            href = urljoin(source.url, href)
        if title and href:
            results.append((title, href))
    return results

def main():
    rows = []
    for src in SOURCES:
        try:
            for title, url in fetch(src):
                rows.append({"source": src.name, "title": title, "url": url})
        except Exception as e:
            print(f"[WARN] {src.name}: {e}")
    with open("output.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "title", "url"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows to output.csv")

if __name__ == "__main__":
    main()