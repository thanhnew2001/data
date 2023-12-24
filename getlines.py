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

# Print the matching headlines
for headline in matching_headlines:
    print(headline)