from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import re
import csv
import time
import urllib.parse

# Company name and symbol list
nifty_companies = [
    ("Adani Enterprises Ltd.", "ADANIENT"),
    ("Adani Ports and Special Economic Zone Ltd.", "ADANIPORTS"),
    ("Apollo Hospitals Enterprise Ltd.", "APOLLOHOSP"),
    ("Asian Paints Ltd.", "ASIANPAINT"),
    ("Axis Bank Ltd.", "AXISBANK"),
    ("Bajaj Auto Ltd.", "BAJAJ-AUTO"),
    ("Bajaj Finance Ltd.", "BAJFINANCE"),
    ("Bajaj Finserv Ltd.", "BAJAJFINSV"),
    ("Bharat Petroleum Corporation Ltd.", "BPCL"),
    ("Bharti Airtel Ltd.", "BHARTIARTL"),
    ("Britannia Industries Ltd.", "BRITANNIA"),
    ("Cipla Ltd.", "CIPLA"),
    ("Coal India Ltd.", "COALINDIA"),
    ("Divi's Laboratories Ltd.", "DIVISLAB"),
    ("Dr. Reddy's Laboratories Ltd.", "DRREDDY"),
    ("Eicher Motors Ltd.", "EICHERMOT"),
    ("Grasim Industries Ltd.", "GRASIM"),
    ("HCL Technologies Ltd.", "HCLTECH"),
    ("HDFC Bank Ltd.", "HDFCBANK"),
    ("HDFC Life Insurance Company Ltd.", "HDFCLIFE"),
    ("Hero MotoCorp Ltd.", "HEROMOTOCO"),
    ("Hindalco Industries Ltd.", "HINDALCO"),
    ("Hindustan Unilever Ltd.", "HINDUNILVR"),
    ("ICICI Bank Ltd.", "ICICIBANK"),
    ("ITC Ltd.", "ITC"),
    ("IndusInd Bank Ltd.", "INDUSINDBK"),
    ("Infosys Ltd.", "INFY"),
    ("JSW Steel Ltd.", "JSWSTEEL"),
    ("Kotak Mahindra Bank Ltd.", "KOTAKBANK"),
    ("LTIMindtree Ltd.", "LTIM"),
    ("Larsen & Toubro Ltd.", "LT"),
    ("Mahindra & Mahindra Ltd.", "M&M"),
    ("Maruti Suzuki India Ltd.", "MARUTI"),
    ("NTPC Ltd.", "NTPC"),
    ("Nestle India Ltd.", "NESTLEIND"),
    ("Oil & Natural Gas Corporation Ltd.", "ONGC"),
    ("Power Grid Corporation of India Ltd.", "POWERGRID"),
    ("Reliance Industries Ltd.", "RELIANCE"),
    ("SBI Life Insurance Company Ltd.", "SBILIFE"),
    ("Shriram Finance Ltd.", "SHRIRAMFIN"),
    ("State Bank of India", "SBIN"),
    ("Sun Pharmaceutical Industries Ltd.", "SUNPHARMA"),
    ("Tata Consultancy Services Ltd.", "TCS"),
    ("Tata Consumer Products Ltd.", "TATACONSUM"),
    ("Tata Motors Ltd.", "TATAMOTORS"),
    ("Tata Steel Ltd.", "TATASTEEL"),
    ("Tech Mahindra Ltd.", "TECHM"),
    ("Titan Company Ltd.", "TITAN"),
    ("UltraTech Cement Ltd.", "ULTRACEMCO"),
    ("Wipro Ltd.", "WIPRO")
]

start_date = "2024-11-01"
end_date = "2024-12-31"

def convert_relative_date(date_str):
    now = datetime.now()
    if "hour" in date_str:
        return (now - timedelta(hours=int(re.search(r'\d+', date_str).group()))).strftime('%d-%m-%Y')
    elif "minute" in date_str:
        return now.strftime('%d-%m-%Y')
    elif "day" in date_str:
        return (now - timedelta(days=int(re.search(r'\d+', date_str).group()))).strftime('%d-%m-%Y')
    elif "week" in date_str:
        return (now - timedelta(weeks=int(re.search(r'\d+', date_str).group()))).strftime('%d-%m-%Y')
    elif "month" in date_str:
        return (now - timedelta(days=int(re.search(r'\d+', date_str).group()) * 30)).strftime('%d-%m-%Y')
    else:
        return date_str

def scrape_page(page, symbol):
    articles = page.query_selector_all('div.SoAPf')
    news = []
    for article in articles:
        try:
            heading = article.query_selector('div.n0jPhd').inner_text()
            source = article.query_selector('div.MgUUmf span').inner_text()
            date = article.query_selector('div.OSrXXb').inner_text()
            formatted_date = convert_relative_date(date)
            news.append([heading, source, formatted_date, symbol])
        except:
            continue
    return news

def save_to_csv(news_data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(['Heading', 'Source', 'Date', 'Symbol'])
        writer.writerows(news_data)

# Main scraping loop
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    combined_news_data = []

    for company_name, symbol in nifty_companies:
        print(f"Scraping news for {company_name} ({symbol})...")
        query = f"{company_name} financial news after:{start_date} before:{end_date}"
        encoded_query = urllib.parse.quote_plus(query)

        page = browser.new_page()
        page.goto(f"https://www.google.com/search?q={encoded_query}&tbm=nws")
        time.sleep(2)

        combined_news_data.extend(scrape_page(page, symbol))

        while True:
            try:
                next_button = page.query_selector('a#pnnext')
                if next_button:
                    next_button.click()
                    page.wait_for_load_state('networkidle')
                    combined_news_data.extend(scrape_page(page, symbol))
                else:
                    break
            except Exception as e:
                print(f"Pagination error for {company_name}: {e}")
                break

        page.close()
        time.sleep(5)

    # Save all collected data into a single CSV
    save_to_csv(combined_news_data, "all_nifty_news_updated.csv")
    print("Saved all company news into all_nifty_news.csv")
    browser.close()