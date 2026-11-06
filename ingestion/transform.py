import json
from datetime import timezone, datetime


def transform(energy_info: dict) -> list[dict]:
    """Convert a ``/v2/price`` response into rows for the raw price table.

    Parameters
    ----------
    energy_info : dict
        Parsed JSON response as returned by ``fetch_price``.

    Returns
    -------
    list of dict
        One dict per element of ``energy_info["data"]``, keyed by column
        name: ``schema_version``, ``country``, ``bidding_zone``,
        ``timezone``, ``interval_minutes``, ``unit``, ``api_generated_at``,
        ``utc_time`` (timezone-aware, in UTC) and ``day_ahead_price``
        (may be ``None``).

    Raises
    ------
    KeyError
        If an expected field is missing from the response.
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
