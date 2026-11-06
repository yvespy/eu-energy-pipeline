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
    """Fetch day-ahead electricity prices from the Energy-Charts API.

    Sends a single GET request to ``/v2/price`` and returns the parsed
    JSON response without any transformation.

    Parameters
    ----------
    zone : str
        Bidding zone code accepted by the API, e.g. ``"DE-LU"``.
    start_date : datetime.date
        First local day to request (inclusive). Sent as ``YYYY-MM-DD``
        and interpreted by the API in local time.
    end_date : datetime.date
        Last local day to request (inclusive). Must not be earlier
        than ``start_date``.

    Returns
    -------
    dict
        Parsed JSON response: an envelope (``schema_version``,
        ``bidding_zone``, ``unit``, ``interval_minutes``, ...) and a
        ``data`` list of ``{"timestamp": ..., "values": ...}`` records.

    Raises
    ------
    requests.HTTPError
        If the API returns a non-success status, e.g. 400 for an invalid
        zone or date range, or 404 when no data is available yet. The
        message contains the status code, request parameters and response
        body; the response itself is available as ``error.response``.
    requests.Timeout
        If the API does not respond within the timeout.
    requests.ConnectionError
        If the connection to the API cannot be established.

    Notes
    -----
    ``interval_minutes`` in the envelope is ``null`` when the requested
    range spans the switch from hourly to 15-minute resolution (between
    2025-09-30 and 2025-10-01). Request one day at a time to avoid this.
    """
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

