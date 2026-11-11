# CodeAlpha Data Analytics Internship Task 1: Web Scraping

This project scrapes book information from [Books to Scrape](https://books.toscrape.com/) and saves the cleaned data into a CSV file.

## Project goals

We will extract the following information from each book:

- Title
- Price
- Availability
- Rating
- Product URL

We will also scrape multiple pages using pagination and save the final dataset as a CSV file.

## Project structure

```text
CodeAlpha_WebScraping/
├── main.py
├── scraper.py
├── requirements.txt
├── README.md
├── data/
│   └── books_dataset.csv
└── .venv/   # optional if you create a virtual environment
```

## Step 1: Create a project folder

Create a folder for your project, then place these files inside it.

## Step 2: Install the required packages

Open a terminal and run:

```bash
pip install requests beautifulsoup4 pandas
```

Or, if you are using requirements.txt:

```bash
pip install -r requirements.txt
```

## Step 3: Understand the code

### main.py
This file runs everything and saves the final dataset.

### scraper.py
This file contains the scraping logic.

- `fetch_page()` downloads the website page.
- `extract_book_data()` takes one product card and extracts the fields.
- `scrape_books()` loops through multiple pages.
- `clean_books_data()` removes unwanted formatting and cleans the values.
- `save_books_dataset()` exports the data to CSV.

## Step 4: Run the scraper

From the project folder, run:

```bash
python main.py
```

The script will:

1. Visit the target pages
2. Grab each book's information
3. Clean the extracted values
4. Save the file in the `data` folder

## Step 5: Check the output

After the script finishes, open the generated CSV file in the `data` folder:

```text
data/books_dataset.csv
```

This file contains the dataset extracted from the website.

## Notes

- The project is beginner-friendly and uses simple libraries.
- The scraper targets real live website data.
- It scrapes multiple pages using page numbers like `page-1.html`, `page-2.html`, and so on.

## Example output

The CSV will contain columns similar to:

```text
title,price,availability,rating,product_url
A Light in the Attic,51.77,In stock,3,https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html
```

## Important

This task uses a website that is designed for scraping practice, so it is useful for learning web scraping safely and ethically.
