from __future__ import annotations

from typing import Any, Dict, List
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/"
SITE_URL = "https://books.toscrape.com/"
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def fetch_page(url: str) -> BeautifulSoup:
    """Fetch a page and return a BeautifulSoup object."""
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_book_data(card: Any) -> Dict[str, Any]:
    """Extract one book's data from a product card."""
    title_tag = card.select_one("h3 a")
    title = title_tag.get("title") or title_tag.get_text(strip=True)

    price_tag = card.select_one("p.price_color")
    price = price_tag.get_text(strip=True) if price_tag else "0.00"

    availability_tag = card.select_one("p.availability")
    availability = availability_tag.get_text(" ", strip=True) if availability_tag else "Unknown"

    rating_tag = card.select_one("p.star-rating")
    rating_class = rating_tag.get("class", ["Unknown"])[1] if rating_tag else "Unknown"
    rating = RATING_MAP.get(rating_class, 0)

    product_url = title_tag.get("href") if title_tag else ""
    product_url = urljoin(BASE_URL, product_url)

    cleaned_price = price.replace("Â", "").replace("£", "").replace(",", "").strip()

    return {
        "title": title.strip(),
        "price": float(cleaned_price),
        "availability": availability,
        "rating": rating,
        "product_url": product_url,
    }


def scrape_books(max_pages: int = 5) -> pd.DataFrame:
    """Scrape multiple pages of books and return them as a DataFrame."""
    records: List[Dict[str, Any]] = []

    for page_number in range(1, max_pages + 1):
        page_url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"
        soup = fetch_page(page_url)

        books = soup.select("article.product_pod")
        if not books:
            break

        for book in books:
            records.append(extract_book_data(book))

    df = pd.DataFrame(records)
    return df


def clean_books_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize the scraped data before saving it as CSV."""
    clean_df = df.copy()
    clean_df = clean_df.dropna(subset=["title"]).reset_index(drop=True)

    if "price" in clean_df.columns:
        clean_df["price"] = (
            clean_df["price"].astype(str).str.replace("£", "", regex=False).str.replace(",", "", regex=False)
        )
        clean_df["price"] = pd.to_numeric(clean_df["price"], errors="coerce")

    if "availability" in clean_df.columns:
        clean_df["availability"] = clean_df["availability"].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()

    if "rating" in clean_df.columns:
        clean_df["rating"] = pd.to_numeric(clean_df["rating"], errors="coerce")

    if "title" in clean_df.columns:
        clean_df["title"] = clean_df["title"].astype(str).str.strip()

    if "product_url" in clean_df.columns:
        clean_df["product_url"] = clean_df["product_url"].astype(str).str.strip()

    return clean_df


def save_books_dataset(df: pd.DataFrame, output_path: str) -> None:
    """Save the DataFrame to a CSV file."""
    df.to_csv(output_path, index=False)
