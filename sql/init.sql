-- Create staging table to handle Yes/No boolean conversion
CREATE TABLE orders_staging (
    order_id          INTEGER,
    order_date        DATE,
    order_time        TIME,
    customer_segment  TEXT,
    order_value       NUMERIC(10, 2),
    cuisine_type      TEXT,
    delivery_time_mins INTEGER,
    promo_code_used   TEXT,
    is_reorder        TEXT
);

-- Load CSV into staging (skip header row)
COPY orders_staging
FROM '/data/campus_bites_orders.csv'
DELIMITER ','
CSV HEADER;

-- Create final table with proper types
CREATE TABLE orders (
    order_id           INTEGER PRIMARY KEY,
    order_date         DATE,
    order_time         TIME,
    customer_segment   TEXT,
    order_value        NUMERIC(10, 2),
    cuisine_type       TEXT,
    delivery_time_mins INTEGER,
    promo_code_used    BOOLEAN,
    is_reorder         BOOLEAN
);

-- Insert with Yes/No -> boolean conversion
INSERT INTO orders
SELECT
    order_id,
    order_date,
    order_time,
    customer_segment,
    order_value,
    cuisine_type,
    delivery_time_mins,
    promo_code_used = 'Yes',
    is_reorder = 'Yes'
FROM orders_staging;

DROP TABLE orders_staging;
