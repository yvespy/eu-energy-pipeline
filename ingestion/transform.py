import json
from datetime import timezone, datetime


def transform(energy_info: dict) -> list[dict]:
    """Transform API response into records for the raw price table.

    Timestamps are converted to UTC.
    """
    result = []
    for item in energy_info["data"]:
        timestamp = datetime.fromisoformat(item["timestamp"])
        utc_time = timestamp.astimezone(timezone.utc)

        result.append({
            "schema_version": energy_info["schema_version"],
            "country": energy_info["country"],
            "bidding_zone": energy_info["bidding_zone"],
            "timezone": energy_info["timezone"],
            "interval_minutes": energy_info["interval_minutes"],
            "unit": energy_info["unit"],
            "api_generated_at": datetime.fromisoformat(energy_info["generated_at"]),
            "utc_time": utc_time,
            "day_ahead_price": item["values"]["day_ahead_price"],
        })
    return result


if __name__ == "__main__":
    with open("./docs/price_dst_fallback_2026-10-25.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
