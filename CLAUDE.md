# Campus Bites Pipeline

Local PostgreSQL database for analyzing campus food delivery orders. The pipeline loads 1,132 orders from a CSV into a Postgres container via Docker.

## Project Structure

- `docker-compose.yml` — spins up the Postgres container
- `sql/init.sql` — runs automatically on first container start; loads the CSV and creates the `orders` table
- `data/campus_bites_orders.csv` — source data (1,132 rows)
- `load_orders.py` — alternative Python script to load the CSV using psycopg2
- `.env` — credentials (not committed); copy from `.env.example`

## Database Connection

| Setting  | Value         |
|----------|---------------|
| Host     | localhost     |
| Port     | 5432          |
| Database | campus_bites  |
| User     | campus_user   |
| Password | campus_pass   |

Connect via psql inside the container:
```bash
docker exec -it campus_bites_db psql -U campus_user -d campus_bites
```

## Schema

**`orders`** table:

| Column              | Type           | Notes                  |
|---------------------|----------------|------------------------|
| order_id            | INTEGER        | Primary key            |
| order_date          | DATE           |                        |
| order_time          | TIME           |                        |
| customer_segment    | TEXT           |                        |
| order_value         | NUMERIC(10,2)  | Dollar amount          |
| cuisine_type        | TEXT           |                        |
| delivery_time_mins  | INTEGER        |                        |
| promo_code_used     | BOOLEAN        | Converted from Yes/No  |
| is_reorder          | BOOLEAN        | Converted from Yes/No  |

## Common Commands

```bash
# Start the database
docker compose up -d

# Stop (preserves data)
docker compose down

# Full reset (deletes all data)
docker compose down -v

# Load data via Python instead of init.sql
python load_orders.py
```
