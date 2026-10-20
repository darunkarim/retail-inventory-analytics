{{ config(materialized='table') }}

WITH sales_30d AS (
    SELECT
        store_id,
        product_id,
        SUM(quantity) AS units_sold_30d,
        SUM(total_amount) AS revenue_30d
    FROM {{ ref('stg_sales') }}
    WHERE sale_date BETWEEN
        (SELECT MAX(sale_date) FROM {{ ref('stg_sales') }}) - INTERVAL 29 DAYS
        AND (SELECT MAX(sale_date) FROM {{ ref('stg_sales') }})
    GROUP BY store_id, product_id
),

inventory AS (
    SELECT * FROM {{ ref('stg_inventory') }}
),

products AS (
    SELECT * FROM {{ ref('stg_products') }}
),

calculated AS (
    SELECT
        i.store_id,
        i.product_id,
        p.product_name,
        p.category,
        i.stock_quantity,
        i.lead_time_days,
        COALESCE(s.units_sold_30d, 0) AS units_sold_30d,
        COALESCE(s.revenue_30d, 0) AS revenue_30d,
        COALESCE(s.units_sold_30d, 0) / 30.0 AS avg_daily_sales,

        CASE
            WHEN COALESCE(s.units_sold_30d, 0) = 0 THEN NULL
            ELSE ROUND(
                i.stock_quantity * 30.0 / s.units_sold_30d, 2
            )
        END AS days_of_cover

    FROM inventory i
    LEFT JOIN sales_30d s
        ON i.store_id = s.store_id
        AND i.product_id = s.product_id
    LEFT JOIN products p
        ON i.product_id = p.product_id
)

SELECT
    *,
    CASE
        WHEN stock_quantity = 0 THEN 'OUT_OF_STOCK'
        WHEN avg_daily_sales = 0 THEN 'NO_SALES'
        WHEN days_of_cover < lead_time_days THEN 'HIGH'
        WHEN days_of_cover < lead_time_days + 3 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS risk_level
FROM calculated
