"""Fetch day-ahead electricity prices from the Energy-Charts API (v2).

Example request::

    https://api.energy-charts.info/v2/price?bzn=DE-LU&start=2026-01-01&end=2026-01-01

where ``/v2/`` is the API version, ``/price`` is the endpoint, ``bzn`` is
the bidding zone and ``start`` / ``end`` are the first and last local day
(dates only; a time can be appended).
"""
from datetime import date

import requests

URL = "https://api.energy-charts.info/v2/price"
TIMEOUT = 5


def fetch_price(zone: str, start_date: date, end_date: date) -> dict:
    """Fetch electricity prices for the specified bidding zone and date range."""
    params = {
        "bzn": zone,
        "start": start_date.isoformat(),
        "end": end_date.isoformat()
    }
    response = requests.get(URL, params=params, timeout=TIMEOUT)
    if not response.ok:
        raise requests.HTTPError(
            f"API request failed: "
            f"status={response.status_code}, "
            f"params={params}, "
            f"message={response.text}",
            response=response
        )
    data = response.json()

    return data


if __name__ == "__main__":
    from ingestion.transform import transform

    raw_data = fetch_price("DE-LU", date(2026, 1, 1), date(2026, 1, 1))
    print(len(transform(raw_data)))
