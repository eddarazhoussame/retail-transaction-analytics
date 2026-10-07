from pathlib import Path
import pandas as pd

# Find the cleaned CSV using the main project folder.
base_dir = Path(__file__).resolve().parents[1]
file_path = base_dir / "data" / "processed" / "transactions_part_01_clean.csv"

# Read the cleaned data into a DataFrame.
df = pd.read_csv(file_path)

# 1. Count all rows in the cleaned data.
print("Total rows:", len(df))

# 2. Count distinct baskets.
print("Total unique baskets:", df["BASKET_ID"].nunique())

# 3. Count distinct customers.
print("Total unique customers:", df["PERSON_PUBLIC_KEY"].nunique())

# 4. Count distinct product categories.
print("Total unique product categories:", df["PRODUCT_CATEGORY"].nunique())

# 5. Count each basket once within its channel.
print("\nBasket count by CHANNEL:")
print(df.groupby("CHANNEL")["BASKET_ID"].nunique())

# 6. Show the 10 product categories with the most rows.
print("\nTop 10 PRODUCT_CATEGORY by row count:")
print(df["PRODUCT_CATEGORY"].value_counts().head(10))

# 7. Count distinct categories in each basket, then calculate the average.
categories_per_basket = df.groupby("BASKET_ID")["PRODUCT_CATEGORY"].nunique()
print("\nAverage product categories per basket:", categories_per_basket.mean())
