import pandas as pd

# Load dataset
file_path = "/Users/mac/recommender_project/api/final_merged_dataset.csv"
df = pd.read_csv(file_path)

# Check for missing values
print("\n🔍 Checking for Missing Values:")
print(df.isnull().sum())

# Check for duplicate rows
print("\n🔍 Checking for Duplicates:")
print(df.duplicated().sum())

# Check if any columns have only one unique value (potentially useless for recommendations)
print("\n🔍 Unique Values per Column:")
print(df.nunique())

# Check for unusual ratings (e.g., negative values or very high values)
print("\n🔍 Checking Rating Distribution:")
print(df["rating"].describe())

# Check if user_id or item_id has very few unique values (which can affect recommendations)
print("\n🔍 Number of Unique Users and Courses:")
print(f"Unique Users: {df['user_id'].nunique()}, Unique Courses: {df['item_id'].nunique()}")
