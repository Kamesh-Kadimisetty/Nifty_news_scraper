# 📰 NIFTY 50 Financial News Scraper

This Python script uses [Playwright](https://playwright.dev/python/) to scrape financial news from **Google News** for all companies in the **NIFTY 50 index** within a specific date range.

It collects news headlines, sources, publication dates, and the related stock symbol, then exports everything into a CSV file.

---

## 📌 Features

- ✅ Scrapes financial news articles for all NIFTY 50 companies.
- ✅ Extracts:
  - Headline
  - News Source
  - Date (converted from relative to absolute)
  - Stock Symbol
- ✅ Supports pagination through search results.
- ✅ Outputs to a clean CSV file: `all_nifty_news_updated.csv`

---

## 🛠 Setup

### 1. Clone the Repo

```bash
git clone [https://github.com/Kamesh-Kadimisetty/nifty-news-scraper](https://github.com/Kamesh-Kadimisetty/Nifty_news_scraper/)
cd nifty-news-scraper
```

### 2. Create & Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # On macOS/Linux
venv\Scripts\activate           # On Windows
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
playwright install
```

### 4. Run the Script
```bash
python scraper.py
```
This will launch a Chromium browser, scrape news data, and save results into : **all_nifty_news_updated.csv**
## 🧾 Example CSV Output

| Heading                                 | Source      | Date       | Symbol   |
|-----------------------------------------|-------------|------------|----------|
| Reliance Q3 profit beats expectations   | ET Markets  | 02-12-2024 | RELIANCE |
| Infosys faces headwinds in US market    | Bloomberg   | 04-12-2024 | INFY     |



