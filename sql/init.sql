CREATE TABLE IF NOT EXISTS iss_location (
    id              SERIAL PRIMARY KEY,
    event_timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    latitude        DOUBLE PRECISION NOT NULL,
    longitude       DOUBLE PRECISION NOT NULL,
    loaded_at       TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT uniq_event_timestamp UNIQUE (event_timestamp)
);
