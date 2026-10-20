SELECT
    CAST(product_id AS VARCHAR) AS product_id,
    CAST(product_name AS VARCHAR) AS product_name,
    CAST(category AS VARCHAR) AS category,
    CAST(unit_price AS DECIMAL(10,2)) AS unit_price
FROM {{ source('raw', 'products') }}
