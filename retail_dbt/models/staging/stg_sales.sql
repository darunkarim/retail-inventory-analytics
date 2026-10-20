SELECT
    CAST(transaction_id AS INTEGER) AS transaction_id,
    CAST(sale_date AS DATE) AS sale_date,
    CAST(store_id AS VARCHAR) AS store_id,
    CAST(product_id AS VARCHAR) AS product_id,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(total_amount AS DECIMAL(12,2)) AS total_amount
FROM {{ source('raw', 'sales') }}
