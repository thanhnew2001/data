import pandas as pd
import glob
import os
import csv
import re

def clean_string(s):
    # Replace multiple spaces with a single space
    return re.sub(r'\s+', ' ', s)

def clean_multiline_headlines(file_path):
    cleaned_data = []

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        current_row = None

        for row in reader:
            if not row or all(not cell.strip() for cell in row):
                continue  # Skip empty rows or rows with all empty cells

            if len(row) == 1:
                # Continuation of a multiline headline
                if current_row:
                    current_row[1] += ' ' + clean_string(row[0])
            else:
                if 'Date not found' in row:
                    continue  # Skip rows containing 'Date not found'

                if current_row:
                    # Add the previous row to the cleaned data
                    cleaned_data.append(current_row)

                current_row = [clean_string(row[0]), clean_string(row[1]), clean_string(row[2])]

        # Don't forget to add the last row
        if current_row:
            cleaned_data.append(current_row)

    return pd.DataFrame(cleaned_data, columns=['date', 'headline', 'link'])

def merge_csv_files(folder_path, output_file):
    # Get a sorted list of all CSV files in the folder
    csv_files = sorted(glob.glob(os.path.join(folder_path, '*.csv')))

    all_data = [clean_multiline_headlines(file) for file in csv_files]

    # Concatenate all dataframes into one
    merged_df = pd.concat(all_data, ignore_index=True)

    # Write the merged DataFrame to a new CSV file
    merged_df.to_csv(output_file, index=False)

# Folder path
folder_path = 'CRAWL_1997_2011'

# Output file name
output_file = 'cleaned_merged_data.csv'

# Merge and clean CSV files and write to a new file
merge_csv_files(folder_path, output_file)
