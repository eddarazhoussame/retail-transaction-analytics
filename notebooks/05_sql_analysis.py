from pathlib import Path
import sqlite3
import pandas as pd

# Locate the database and create the folder for the CSV results.
base_dir = Path(__file__).resolve().parents[1]
database_path = base_dir / "SQL" / "retail_analytics.db"
output_dir = base_dir / "data" / "processed" / "sql_outputs"
output_dir.mkdir(parents=True, exist_ok=True)

# Check the database exists before connecting to it.
if not database_path.is_file():
    raise FileNotFoundError(f"Database not found: {database_path}")

# Store each SQL query with the name of its output file.
queries = {
    # 1. Count rows and distinct baskets, customers, and categories.
    "kpi_summary.csv": """
        SELECT
            COUNT(*) AS total_rows,
            COUNT(DISTINCT BASKET_ID) AS total_unique_baskets,
            COUNT(DISTINCT PERSON_PUBLIC_KEY) AS total_unique_customers,
            COUNT(DISTINCT PRODUCT_CATEGORY) AS total_unique_product_categories
        FROM transactions
    """,

    # 2. Count unique baskets per channel and their share of all baskets.
    "channel_summary.csv": """
        SELECT
            CHANNEL,
            COUNT(DISTINCT BASKET_ID) AS basket_count,
            ROUND(
                100.0 * COUNT(DISTINCT BASKET_ID) /
                NULLIF((SELECT COUNT(DISTINCT BASKET_ID) FROM transactions), 0),
                2
            ) AS percentage_share
        FROM transactions
        GROUP BY CHANNEL
        ORDER BY basket_count DESC, CHANNEL
    """,

    # 3. DISTINCT counts each category only once within a basket.
    "category_summary.csv": """
        SELECT
            PRODUCT_CATEGORY,
            COUNT(DISTINCT BASKET_ID) AS basket_count
        FROM transactions
        WHERE PRODUCT_CATEGORY IS NOT NULL
        GROUP BY PRODUCT_CATEGORY
        ORDER BY basket_count DESC, PRODUCT_CATEGORY
        LIMIT 15
    """,

    # 4. Count distinct categories per basket, then count baskets of each size.
    "basket_size_summary.csv": """
        WITH basket_sizes AS (
            SELECT
                BASKET_ID,
                COUNT(DISTINCT PRODUCT_CATEGORY) AS category_count
            FROM transactions
            WHERE BASKET_ID IS NOT NULL
            GROUP BY BASKET_ID
        )
        SELECT
            category_count,
            COUNT(*) AS basket_count
        FROM basket_sizes
        GROUP BY category_count
        ORDER BY category_count
    """,

    # 5. Find the 10 customers with the most unique baskets.
    "customer_summary.csv": """
        SELECT
            PERSON_PUBLIC_KEY,
            COUNT(DISTINCT BASKET_ID) AS basket_count
        FROM transactions
        WHERE PERSON_PUBLIC_KEY IS NOT NULL
        GROUP BY PERSON_PUBLIC_KEY
        ORDER BY basket_count DESC, PERSON_PUBLIC_KEY
        LIMIT 10
    """,

    # 6. Measure each category's performance by unique baskets in each channel.
    "category_by_channel_summary.csv": """
        SELECT
            CHANNEL,
            PRODUCT_CATEGORY,
            COUNT(DISTINCT BASKET_ID) AS basket_count
        FROM transactions
        WHERE PRODUCT_CATEGORY IS NOT NULL
        GROUP BY CHANNEL, PRODUCT_CATEGORY
        ORDER BY CHANNEL, basket_count DESC, PRODUCT_CATEGORY
    """,
}

# Run each query with pandas and save its result without a DataFrame index.
connection = sqlite3.connect(database_path)
try:
    for filename, query in queries.items():
        result = pd.read_sql_query(query, connection)
        output_path = output_dir / filename
        result.to_csv(output_path, index=False)

        # Print the exported path and preview the first five rows.
        print("\nExported file:", output_path)
        print(result.head().to_string(index=False))
finally:
    # Always close the database connection when finished.
    connection.close()  
