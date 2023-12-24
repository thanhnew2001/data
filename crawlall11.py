import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def save_to_csv(data, csv_file_path):
    # Save data to a CSV file
    df = pd.DataFrame(data)
    df.to_csv(csv_file_path, index=False)

def fetch_article_date(article):
    date_element = article.find('span', class_='article__timestamp')
    if date_element:
        return date_element.text.strip()
    else:
        return 'Date not found'

def fetch_and_save_monthly_news(start_date, end_date, base_url, max_pages=600):
    monthly_data = []
    for page in range(0, max_pages + 1):
        formatted_start_date = start_date.strftime('%m%%2F%d%%2F%Y')
        formatted_end_date = end_date.strftime('%m%%2F%d%%2F%Y')
        search_url = f"{base_url}&sd={formatted_start_date}&ed={formatted_end_date}&pageNumber={page}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        no_results_message = soup.find(text="No results found. Please run a search to see results.")
        if no_results_message:
            break  # Skip the rest of the pages for this month

        articles = soup.find_all('div', class_='element--article')
        for article in articles:
            headline = article.find('h3')
            if headline:
                article_date = fetch_article_date(article)
                news_data = {
                    'date': article_date,
                    'headline': headline.text.strip(),
                    'link': article.find('a')['href']
                }
                monthly_data.append(news_data)
        time.sleep(1)
    
    return monthly_data

# Define the date range <|{state}|toggle|lov=Off;On|on_change=toggle_state|>

start_date = datetime(1997, 1, 1)
end_date = datetime(2009, 5, 31)

# Define the base URL for the AJAX request
base_url = "https://www.marketwatch.com/search/moreHeadlines?q=NOT%22fuck%22&ts=5&partial=true&tab=All%20News"

# Iterate over each month and fetch news
current_date = start_date
while current_date < end_date:
    month_end = (current_date + pd.offsets.MonthEnd(1)).to_pydatetime()
    monthly_news = fetch_and_save_monthly_news(current_date, month_end, base_url)
    
    if monthly_news:
        # Save the monthly data to a file
        file_name = f"CRAWL_{current_date.strftime('%Y_%m')}.csv"
        save_to_csv(monthly_news, file_name)

    current_date = (month_end + pd.DateOffset(days=1)).to_pydatetime()

print("Data saved for each month.")
