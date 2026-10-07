from pathlib import Path
import pandas as pd

# Read the cleaned CSV from the main project folder.
base_dir = Path(__file__).resolve().parents[1]
file_path = base_dir / "data" / "processed" / "transactions_part_01_clean.csv"
df = pd.read_csv(file_path)

# Create the folder for the result tables if it does not exist.
output_dir = base_dir / "data" / "processed" / "analysis_outputs"
output_dir.mkdir(parents=True, exist_ok=True)

# 1. Count unique baskets by channel and calculate percentage share.
channel_summary = (
    df.groupby("CHANNEL", dropna=False)["BASKET_ID"]
    .nunique()
    .reset_index(name="basket_count")
    .sort_values("basket_count", ascending=False)
)
channel_summary["percentage_share"] = (
    channel_summary["basket_count"] / channel_summary["basket_count"].sum() * 100
).round(2)
print("\nBasket count and percentage share by channel:")
print(channel_summary.to_string(index=False))

# 2. Count each category only once per basket and show the top 15.
category_summary = (
    df.groupby("PRODUCT_CATEGORY")["BASKET_ID"]
    .nunique()
    .reset_index(name="basket_count")
    .sort_values("basket_count", ascending=False)
    .head(15)
)
print("\nTop 15 product categories by unique basket count:")
print(category_summary.to_string(index=False))

# 3. Count distinct categories per basket, then find the average and median.
categories_per_basket = df.groupby("BASKET_ID")["PRODUCT_CATEGORY"].nunique()
basket_size_summary = pd.DataFrame({
    "average_categories_per_basket": [categories_per_basket.mean()],
    "median_categories_per_basket": [categories_per_basket.median()],
})
print("\nProduct categories per basket:")
print(basket_size_summary.to_string(index=False))

# 4. Count unique baskets for each customer.
baskets_per_customer = df.groupby("PERSON_PUBLIC_KEY")["BASKET_ID"].nunique()
top_customers = (
    baskets_per_customer.sort_values(ascending=False)
    .head(10)
    .reset_index(name="basket_count")
)
top_customers["metric"] = "top_customer"

# Save the average, median, and top 10 customers together in one table.
customer_averages = pd.DataFrame({
    "metric": ["average", "median"],
    "PERSON_PUBLIC_KEY": ["", ""],
    "basket_count": [baskets_per_customer.mean(), baskets_per_customer.median()],
})
customer_summary = pd.concat([customer_averages, top_customers], ignore_index=True)
print("\nBaskets per customer: average, median, and top 10 customers:")
print(customer_summary.to_string(index=False))

# 5. Show the top 15 categories within each channel by unique basket count.
category_by_channel_summary = (
    df.groupby(["CHANNEL", "PRODUCT_CATEGORY"])["BASKET_ID"]
    .nunique()
    .reset_index(name="basket_count")
    .sort_values(["CHANNEL", "basket_count"], ascending=[True, False])
    .groupby("CHANNEL")
    .head(15)
)
print("\nTop product categories by channel:")
print(category_by_channel_summary.to_string(index=False))

# Save all five result tables without the DataFrame index.
channel_summary.to_csv(output_dir / "channel_summary.csv", index=False)
category_summary.to_csv(output_dir / "category_summary.csv", index=False)
basket_size_summary.to_csv(output_dir / "basket_size_summary.csv", index=False)
customer_summary.to_csv(output_dir / "customer_summary.csv", index=False)
category_by_channel_summary.to_csv(output_dir / "category_by_channel_summary.csv", index=False)

print("\nAnalysis tables saved successfully")
print(output_dir)
