
ALTER TABLE dwh.fact_flights
ADD CONSTRAINT fact_flights_date_fk
FOREIGN KEY (flight_date)
REFERENCES dwh.dim_date (date_id);
