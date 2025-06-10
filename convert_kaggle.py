import pandas as pd

# ✅ Update file name correctly (add extension!)
input_path = "training.1600000.processed.noemoticon.csv"  # or .xlsx if Excel
output_path = "sample_tweets.csv"

# These are the columns of the Kaggle tweet dataset
columns = ['sentiment', 'id', 'date', 'query', 'user', 'text']

# Load only text-related columns
df = pd.read_csv(input_path, encoding='latin-1', names=columns)

# Save a sample for testing
df[['text']].head(500).to_csv(output_path, index=False)

print("✅ sample_tweets.csv created successfully!")
