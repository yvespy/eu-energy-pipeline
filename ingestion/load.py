import json
import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2 import extras

from ingestion.transform import transform

load_dotenv()

COLUMNS = (
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
    return [
        tuple(row[col] for col in COLUMNS)
        for row in data
    ]


def load_to_db(transformed_data: list[tuple]) -> None:
    conn = None

    try:
        conn = psycopg2.connect(
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
        )

        query = (
            f"INSERT INTO raw.energy_charts_price ({', '.join(COLUMNS)}) "
            "VALUES %s "
            "ON CONFLICT (bidding_zone, utc_time) "
            "DO UPDATE SET "
            "day_ahead_price = EXCLUDED.day_ahead_price, "
            "api_generated_at = EXCLUDED.api_generated_at "
            "WHERE "
            "raw.energy_charts_price.day_ahead_price "
            "IS DISTINCT FROM EXCLUDED.day_ahead_price"
        )
        with conn:
            with conn.cursor() as cur:
                extras.execute_values(cur, query, transformed_data)
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    file_path = Path(__file__).resolve().parent.parent / "docs" / "price_dst_fallback_2026-10-25.json"

    with file_path.open("r", encoding="utf-8") as f:
        json_data = json.load(f)

    transform_data = transform(json_data)
    load_to_db(convert_data_for_load(transform_data))
