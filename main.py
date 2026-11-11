from pathlib import Path

from scraper import clean_books_data, save_books_dataset, scrape_books


def main() -> None:
    """Run the scraping process and save the cleaned data to a CSV file."""
    project_dir = Path(__file__).resolve().parent
    data_dir = project_dir / "data"
    data_dir.mkdir(exist_ok=True)

    raw_df = scrape_books(max_pages=5)
    cleaned_df = clean_books_data(raw_df)

    output_file = data_dir / "books_dataset.csv"
    save_books_dataset(cleaned_df, str(output_file))

    print(f"Scraping complete. {len(cleaned_df)} books saved to {output_file}")


if __name__ == "__main__":
    main()
