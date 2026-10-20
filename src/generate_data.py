
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

STORES = ["STORE_001", "STORE_002", "STORE_003"]
PRODUCTS = [f"PROD_{i:03d}" for i in range(1, 21)]
END_DATE = date(2026, 10, 19)


def write_csv(filename, columns, rows):
    path = DATA_DIR / filename
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {filename}: {len(rows)} rows")


# Product master data
products = [
    {
        "product_id": product,
        "product_name": f"Product {i}",
        "category": ["Shoes", "Clothing", "Accessories"][i % 3],
        "unit_price": random.randint(199, 1499),
    }
    for i, product in enumerate(PRODUCTS, start=1)
]

write_csv(
    "products.csv",
    ["product_id", "product_name", "category", "unit_price"],
    products,
)


# Sales transactions over 30 days
sales = []
transaction_id = 1

for days_ago in range(29, -1, -1):
    sale_date = END_DATE - timedelta(days=days_ago)

    for store in STORES:
        for product in products:
            quantity = random.randint(0, 8)

            if quantity == 0:
                continue

            sales.append({
                "transaction_id": transaction_id,
                "sale_date": sale_date.isoformat(),
                "store_id": store,
                "product_id": product["product_id"],
                "quantity": quantity,
                "total_amount": quantity * product["unit_price"],
            })
            transaction_id += 1

write_csv(
    "sales.csv",
    [
        "transaction_id", "sale_date", "store_id",
        "product_id", "quantity", "total_amount"
    ],
    sales,
)


# Current inventory snapshot
inventory = []

for store in STORES:
    for product in PRODUCTS:
        inventory.append({
            "store_id": store,
            "product_id": product,
            "stock_quantity": random.randint(0, 100),
            "lead_time_days": random.randint(3, 14),
            "snapshot_date": END_DATE.isoformat(),
        })

write_csv(
    "inventory.csv",
    [
        "store_id", "product_id", "stock_quantity",
        "lead_time_days", "snapshot_date"
    ],
    inventory,
)

print("Synthetic retail dataset generated successfully!")
