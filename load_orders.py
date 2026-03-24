import csv
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

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

INSERT_SQL = """
INSERT INTO orders (
    order_id, order_date, order_time, customer_segment,
    order_value, cuisine_type, delivery_time_mins, promo_code_used, is_reorder
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (order_id) DO NOTHING;
"""

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "campus_bites_orders.csv")


def parse_bool(value):
    return value.strip().lower() == "yes"


def main():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    with conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE_SQL)
            print("Table 'orders' ready.")

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

            cur.executemany(INSERT_SQL, rows)
            print(f"Inserted {cur.rowcount} rows into 'orders'.")

    conn.close()


if __name__ == "__main__":
    main()
