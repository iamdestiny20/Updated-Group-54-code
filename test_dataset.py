
import pandas as pd

# Load dataset
file_path = "/Users/mac/recommender_project/api/final_merged_dataset.csv"  # Ensure correct path
df = pd.read_csv(file_path)

# Display basic info
print("✅ Dataset Loaded Successfully!")
print(df.info())  # Shows column details
print(df.head())  # Shows first few rows
