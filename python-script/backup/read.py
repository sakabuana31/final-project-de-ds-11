import pandas as pd

# Create an iterator that reads the file in chunks
json_iterator = pd.read_json('yelp_academic_dataset_review.json', chunksize=100000, lines=True)

# Iterate over the chunks and process the data
for json_chunk in json_iterator:
    # Do whatever processing you need to do with the data in the chunk
    # For example, you can print the column names using the `columns` attribute
    print(json_chunk.columns)