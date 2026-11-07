import json
import os

from psycopg2 import extras

from ingestion.transform import transform
import psycopg2
from dotenv import load_dotenv

load_dotenv()

columns = (
    "schema_version",
    "country",
    "bidding_zone",
    "timezone",
    "interval_minutes",
    "unit",
    "api_generated_at",
    "utc_time",
    "day_ahead_price"
)


def convert_data_for_load(data: list[dict]) -> list[tuple]:
    result = [tuple(row.values()) for row in data]
    return result


def load_to_db(transformed_data: list[tuple]) -> None:
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )

    cur = conn.cursor()
    query = f"INSERT INTO raw.energy_charts_price ({', '.join(columns)}) VALUES %s"
    extras.execute_values(cur, query, transformed_data)
    conn.commit()

    cur.close()
    conn.close()


if __name__ == "__main__":
    with open("../docs/price_dst_fallback_2026-10-25.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    transform_data = transform(json_data)
    load_to_db(convert_data_for_load(transform_data))
