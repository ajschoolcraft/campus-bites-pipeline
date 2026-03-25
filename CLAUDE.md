# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Local PostgreSQL database for analyzing campus food delivery orders. The database holds 1,132 orders loaded from a CSV. Primary use case is interactive SQL queries.

## Commands

```bash
# Start Postgres container
docker compose up -d

# Load/reload data (creates table if needed, idempotent)
python load_orders.py

# Connect via psql
docker exec -it campus_bites_db psql -U campus_user -d campus_bites

# Stop (preserves data)
docker compose down

# Full reset (deletes volume, next `up -d` starts fresh)
docker compose down -v
```

## Database Connection

Host: localhost, Port: 5432, Database: campus_bites, User: campus_user, Password: campus_pass

Credentials are stored in `.env` (copied from `.env.example`). The Docker container and `load_orders.py` both read from this file.

## Schema

Single table: **`orders`** (1,132 rows)

| Column | Type | Notes |
|---|---|---|
| order_id | INTEGER | Primary key |
| order_date | DATE | |
| order_time | TIME | |
| customer_segment | TEXT | |
| order_value | NUMERIC(10,2) | Dollar amount |
| cuisine_type | TEXT | |
| delivery_time_mins | INTEGER | |
| promo_code_used | BOOLEAN | CSV has Yes/No, converted by load script |
| is_reorder | BOOLEAN | CSV has Yes/No, converted by load script |

## Architecture

- **`docker-compose.yml`** — Postgres 15 container. Mounts `./data` to `/data` inside the container. Uses a named volume `pgdata` for persistence.
- **`load_orders.py`** — Python script that creates the `orders` table and loads `data/campus_bites_orders.csv` using psycopg2. Idempotent: uses `CREATE TABLE IF NOT EXISTS` and `ON CONFLICT DO NOTHING`. Reads DB credentials from `.env` via python-dotenv.
- **`data/campus_bites_orders.csv`** — Source data. Boolean columns use Yes/No strings.

## Python Dependencies

Requires `psycopg2-binary` and `python-dotenv`. A virtualenv exists at `venv/`.
