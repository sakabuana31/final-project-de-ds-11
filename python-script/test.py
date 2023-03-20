# %%
import pandas as pd
import numpy as np

# %%
# Load the other file with business IDs
df = pd.read_csv('../data/output-csv/business_restaurant.csv')
# Get a list of business IDs from the other file
other_business_ids = df['business_id'].tolist()


# %%
# Create an iterator that reads the file in chunks
json_iterator = pd.read_json('../data/yelp-dataset/yelp_academic_dataset_review.json', chunksize=100000, lines=True)

# Iterate over the chunks and process the data
for json_chunk_review in json_iterator:
    # Filter out rows with business IDs not in the other file
    json_chunk_review = json_chunk_review[json_chunk_review['business_id'].isin(other_business_ids)]

    print(f"Number of rows in chunk: {len(json_chunk_review)}")
    print(json_chunk_review.head(5))
    if len(json_chunk_review) < 100000:
        break

# %%
# Define a function to format the date string
def format_date(date_str):
    date = pd.to_datetime(date_str, format='%Y-%m-%d %H:%M:%S')
    return date.strftime('%Y%m%d')

# Apply the function to the 'date_values' column of the DataFrame and create a new column
json_chunk_review['date_values'] = json_chunk_review['date'].apply(format_date)

# %%
# Drop the 'date' column from the DataFrame
json_chunk_review.drop(columns=['date'], inplace=True)
json_chunk_review['stars'] = pd.to_numeric(json_chunk_review['stars'], errors='coerce')
json_chunk_review['stars'] = json_chunk_review['stars'].replace('', None)
json_chunk_review.dropna(subset=['stars'], inplace=True)

# %%
json_chunk_review

# %%
json_chunk_review.info()

# %%
# Save DataFrame to CSV file
json_chunk_review.to_csv('../data/output-csv/review_restaurant.csv', index=False)


