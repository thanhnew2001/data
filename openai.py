import requests
import json

# Replace 'your-api-key' with your actual OpenAI API key
api_key="sk-"


headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

import csv

def get_headlines_with_date(filename):
    headlines = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) > 1:
                headline = row[1]  # Assuming headline is in the first column
                date = row[0]  # Assuming date is in the second column
                if date and "Aug" in date and "1997" in date:
                    headlines.append(headline)
    return headlines

# Usage
filename = "cleaned_merged_data.csv"

# Get headlines with the target date condition and skip empty rows
matching_headlines = get_headlines_with_date(filename)
lines = '\n'.join(matching_headlines)
print(lines)

# Print the matching headlines
# for headline in matching_headlines:
#     print(headline)

prompt = f"""
You are finance reporter. Here are a list of headlines news related to economics, finance, stock, market, etc. 
{lines}
You write each headline an essay whose length is 100 words max to elaborate the headlines.
You don't need to be creative. Stick to the fact and knowledge that you know.
"""
print(prompt)

data = {
    "model": "gpt-3.5-turbo",  # Specify the model you are using
    "messages": [
        {"role": "system", "content": f"{prompt}"},
    ]
}

response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))

print(response.text)  # Prints the response from the API
