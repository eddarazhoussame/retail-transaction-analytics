from pathlib import Path
import sqlite3
import pandas as pd

# Find the CSV and database paths using the main project folder.
base_dir = Path(__file__).resolve().parents[1]
file_path = base_dir / "data" / "processed" / "transactions_part_01_clean.csv"
database_path = base_dir / "SQL" / "retail_analytics.db"

# Read the cleaned CSV into a DataFrame.
df = pd.read_csv(file_path)

# Create or open the database and replace the transactions table.
connection = sqlite3.connect(database_path)
try:
    df.to_sql("transactions", connection, if_exists="replace", index=False)
finally:
    connection.close()

# Reconnect to the database to check the saved table.
connection = sqlite3.connect(database_path)
try:
    # 1. Count the rows in the transactions table.
    row_count = connection.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    print("Number of rows:", row_count)

    # 2. Read and print the first five rows.
    first_five_rows = pd.read_sql_query("SELECT * FROM transactions LIMIT 5", connection)
    print("\nFirst 5 rows:")
    print(first_five_rows.to_string(index=False))

    # 3. Print the column names returned by the table query.
    print("\nTable column names:")
    print(first_five_rows.columns.tolist())
finally:
    # Close the database connection when finished.
    connection.close()
