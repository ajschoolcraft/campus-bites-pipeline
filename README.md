# Campus Bites Pipeline

Local Postgres database for analyzing campus food delivery orders.

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Setup

**1. Clone the repo**
```bash
git clone <repo-url>
cd campus-bites-pipeline
```

**2. Create your `.env` file**
```bash
cp .env.example .env
```
You can leave the defaults as-is or change them.

**3. Start the database**
```bash
docker compose up -d
```

On first startup, Postgres will automatically create the `orders` table and load all 1,132 rows from the CSV. This takes about 10–15 seconds.

**4. Connect and query**

Using the Postgres CLI inside the container:
```bash
docker exec -it campus_bites_db psql -U campus_user -d campus_bites
```

Or connect from any SQL client (DBeaver, TablePlus, etc.) with:
| Setting  | Value       |
|----------|-------------|
| Host     | localhost   |
| Port     | 5432        |
| Database | campus_bites |
| User     | campus_user |
| Password | campus_pass |

## Example Queries

```sql
-- Preview the data
SELECT * FROM orders LIMIT 10;

-- Average order value by cuisine
SELECT cuisine_type, ROUND(AVG(order_value), 2) AS avg_value
FROM orders
GROUP BY cuisine_type
ORDER BY avg_value DESC;

-- Promo code usage rate
SELECT promo_code_used, COUNT(*) AS count
FROM orders
GROUP BY promo_code_used;
```

## Stopping / Resetting

```bash
# Stop the container (data is preserved)
docker compose down

# Stop and delete all data (full reset)
docker compose down -v
```

To reload the CSV from scratch, run the full reset above and then `docker compose up -d` again.
