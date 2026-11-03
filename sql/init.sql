CREATE SCHEMA IF NOT EXISTS raw;
CREATE TABLE IF NOT EXISTS raw.energy_charts_price (
    schema_version VARCHAR(80) NOT NULL,
    country VARCHAR(80) NOT NULL,
    bidding_zone VARCHAR(80) NOT NULL,
    timezone VARCHAR(80) NOT NULL,
    interval_minutes INT NOT NULL,
    unit VARCHAR(80) NOT NULL,
    api_generated_at timestamptz NOT NULL,
    utc_time timestamptz NOT NULL,
    day_ahead_price numeric,
    PRIMARY KEY (bidding_zone, utc_time)
);