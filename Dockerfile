FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DBT_PROFILES_DIR=/app/.dbt
ENV DUCKDB_PATH=/app/data/retail.duckdb

CMD ["python", "run_pipeline.py"]
