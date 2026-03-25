# ---------------------------------------------------------------------------
# load_orders.py — Reads the campus_bites_orders CSV and loads it into
# the 'orders' table in the local Postgres database.
# ---------------------------------------------------------------------------

import csv
import os
import psycopg2
from dotenv import load_dotenv

# Read database credentials from the .env file (POSTGRES_DB, POSTGRES_USER, etc.)
load_dotenv()

# SQL to create the orders table if it doesn't already exist.
# Uses IF NOT EXISTS so the script is safe to run repeatedly.
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS orders (
    order_id            INTEGER PRIMARY KEY,
    order_date          DATE,
    order_time          TIME,
    customer_segment    VARCHAR(50),
    order_value         NUMERIC(10, 2),
    cuisine_type        VARCHAR(50),
    delivery_time_mins  INTEGER,
    promo_code_used     BOOLEAN,
    is_reorder          BOOLEAN
);
"""

# SQL to insert a single row. ON CONFLICT (order_id) DO NOTHING makes
# the script idempotent — re-running it won't create duplicate rows.
INSERT_SQL = """
INSERT INTO orders (
    order_id, order_date, order_time, customer_segment,
    order_value, cuisine_type, delivery_time_mins, promo_code_used, is_reorder
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (order_id) DO NOTHING;
"""

# Build an absolute path to the CSV so the script works regardless of
# which directory it's run from.
CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "campus_bites_orders.csv")


def parse_bool(value):
    """Convert 'Yes'/'No' strings from the CSV into Python booleans."""
    return value.strip().lower() == "yes"


def main():
    # Connect to the local Postgres instance using credentials from .env
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    # Use `with conn` to wrap everything in a transaction — if anything
    # fails, all changes are rolled back automatically.
    with conn:
        with conn.cursor() as cur:
            # Create the table (no-op if it already exists)
            cur.execute(CREATE_TABLE_SQL)
            print("Table 'orders' ready.")

            # Read the CSV and convert each row into a tuple of properly
            # typed Python values that psycopg2 can pass to Postgres.
            with open(CSV_PATH, newline="") as f:
                reader = csv.DictReader(f)
                rows = [
                    (
                        int(row["order_id"]),
                        row["order_date"],
                        row["order_time"],
                        row["customer_segment"],
                        float(row["order_value"]),
                        row["cuisine_type"],
                        int(row["delivery_time_mins"]),
                        parse_bool(row["promo_code_used"]),
                        parse_bool(row["is_reorder"]),
                    )
                    for row in reader
                ]

            # Insert all rows in one batch. executemany sends one INSERT
            # per row but within a single transaction, so it's all-or-nothing.
            cur.executemany(INSERT_SQL, rows)
            print(f"Inserted {cur.rowcount} rows into 'orders'.")

    conn.close()


if __name__ == "__main__":
    main()
