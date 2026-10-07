from pathlib import Path
import pandas as pd

# This gives us the main project folder
base_dir = Path(__file__).resolve().parents[1]

# This is the path to the raw CSV file
file_path = base_dir / "data" / "Raw" / "transactions_part_01.csv"

print("File path:")
print(file_path)

print("\nFile exists?")
print(file_path.exists())

# Read the CSV file with pandas
df = pd.read_csv(file_path)

print("\nShape:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())

# 1. Show the name of each column in the dataset.
print("\nColumns:")
print(df.columns)

# 2. Show the data type pandas assigned to each column.
print("\nData types:")
print(df.dtypes)

# 3. Count missing values in each column.
print("\nMissing values:")
print(df.isnull().sum())

# 4. Count repeated rows after their first occurrence, comparing all columns.
print("\nDuplicate rows:")
print(df.duplicated().sum())

# 5. Count rows for each CHANNEL, including any missing values.
print("\nCHANNEL value counts:")
print(df["CHANNEL"].value_counts(dropna=False))

# 6. Show the 10 most frequent PRODUCT_CATEGORY values and their row counts.
print("\nTop 10 PRODUCT_CATEGORY values:")
print(df["PRODUCT_CATEGORY"].value_counts().head(10))

# Count the rows before cleaning.
print("\nRows before cleaning:", len(df))

# Remove exact duplicate rows and store the result in a new DataFrame.
df_clean = df.drop_duplicates()

# Show the remaining rows and how many duplicate rows were removed.
print("Rows after cleaning:", len(df_clean))
print("Duplicate rows removed:", len(df) - len(df_clean))

# Copy the cleaned data before adding a new column.
df_clean = df_clean.copy()

# Combine customer, date, and channel to identify each basket.
df_clean["BASKET_ID"] = (
    df_clean["PERSON_PUBLIC_KEY"].astype(str)
    + "_"
    + df_clean["DATE"].astype(str)
    + "_"
    + df_clean["CHANNEL"].astype(str)
)

# Count unique baskets, customers, and product categories.
print("\nUnique baskets:", df_clean["BASKET_ID"].nunique())
print("Unique customers:", df_clean["PERSON_PUBLIC_KEY"].nunique())
print("Unique product categories:", df_clean["PRODUCT_CATEGORY"].nunique())

# Count each basket once within its channel.
print("\nBasket count by CHANNEL:")
print(df_clean.groupby("CHANNEL")["BASKET_ID"].nunique())

# Show the 10 most frequent product categories in the cleaned data.
print("\nTop 10 PRODUCT_CATEGORY values after cleaning:")
print(df_clean["PRODUCT_CATEGORY"].value_counts().head(10))

# Save the cleaned data to CSV without the DataFrame index.
output_path = base_dir / "data" / "processed" / "transactions_part_01_clean.csv"
df_clean.to_csv(output_path, index=False)

# Confirm the save and show the output file path.
print("Clean file saved successfully")
print(output_path)
