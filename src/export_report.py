
from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "retail.duckdb"
REPORT_DIR = BASE_DIR / "reports"
REPORT_PATH = REPORT_DIR / "inventory_risk.csv"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

query = """
SELECT
    store_id,
    product_id,
    product_name,
    category,
    stock_quantity,
    units_sold_30d,
    ROUND(avg_daily_sales, 2) AS avg_daily_sales,
    days_of_cover,
    lead_time_days,
    risk_level
FROM main.mart_inventory_risk
ORDER BY
    CASE risk_level
        WHEN 'OUT_OF_STOCK' THEN 1
        WHEN 'HIGH' THEN 2
        WHEN 'MEDIUM' THEN 3
        WHEN 'LOW' THEN 4
        ELSE 5
    END,
    days_of_cover ASC NULLS LAST
"""

with duckdb.connect(str(DB_PATH), read_only=True) as conn:
    result = conn.execute(query)
    rows = result.fetchall()
    columns = [column[0] for column in result.description]

import csv

with REPORT_PATH.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(columns)
    writer.writerows(rows)

print(f"Report exported: {REPORT_PATH}")
print(f"Total rows: {len(rows)}")
