
from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "raw"
DB_PATH = BASE_DIR / "data" / "retail.duckdb"

TABLES = {
    "products": "products.csv",
    "sales": "sales.csv",
    "inventory": "inventory.csv",
}


def ingest_data():
    conn = duckdb.connect(str(DB_PATH))

    try:
        conn.execute("CREATE SCHEMA IF NOT EXISTS raw")

        for table, filename in TABLES.items():
            file_path = DATA_DIR / filename

            if not file_path.exists():
                raise FileNotFoundError(
                    f"Missing source file: {file_path}"
                )

            print(f"Loading {filename}...")

            conn.execute(
                f"""
                CREATE OR REPLACE TABLE raw.{table} AS
                SELECT *
                FROM read_csv_auto(?)
                """,
                [str(file_path)],
            )

            count = conn.execute(
                f"SELECT COUNT(*) FROM raw.{table}"
            ).fetchone()[0]

            print(f"Loaded raw.{table}: {count} rows")

        print("\nIngestion completed successfully!")

    finally:
        conn.close()


if __name__ == "__main__":
    ingest_data()
