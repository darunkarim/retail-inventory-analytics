
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

os.environ["DBT_PROFILES_DIR"] = str(ROOT / ".dbt")
os.environ["DUCKDB_PATH"] = str(ROOT / "data" / "retail.duckdb")


def run(command):
    print(f"\nRunning: {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


run([sys.executable, "src/generate_data.py"])
run([sys.executable, "src/ingest_data.py"])

run([
    "dbt", "build",
    "--project-dir", "retail_dbt",
    "--profiles-dir", ".dbt"
])

run([sys.executable, "src/export_report.py"])

print("\nPipeline completed successfully!")
