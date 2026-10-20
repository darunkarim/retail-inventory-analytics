SELECT
    CAST(store_id AS VARCHAR) AS store_id,
    CAST(product_id AS VARCHAR) AS product_id,
    CAST(stock_quantity AS INTEGER) AS stock_quantity,
    CAST(lead_time_days AS INTEGER) AS lead_time_days,
    CAST(snapshot_date AS DATE) AS snapshot_date
FROM {{ source('raw', 'inventory') }}
