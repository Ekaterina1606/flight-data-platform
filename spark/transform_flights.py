
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    explode,
    to_timestamp,
    when,
)

# Create Spark session
spark = (
    SparkSession.builder
    .appName("FlightDataPlatform")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# Read JSON file
file_path = "data/raw/flights/flights.json"

df = spark.read.json(file_path, multiLine=True)

# Extract individual flights
df = df.select(explode(col("data")).alias("flight"))

# Flatten nested JSON fields
flights = df.select(
    col("flight.flight_date").cast("date").alias("flight_date"),
    col("flight.flight_status").alias("flight_status"),
    col("flight.airline.name").alias("airline_name"),
    col("flight.flight.iata").alias("flight_iata"),
    col("flight.departure.iata").alias("departure_iata"),
    col("flight.departure.airport").alias("departure_airport"),
    to_timestamp(
        col("flight.departure.scheduled")
    ).alias("scheduled_departure"),
    col("flight.arrival.iata").alias("arrival_iata"),
    col("flight.arrival.airport").alias("arrival_airport"),
    to_timestamp(
        col("flight.arrival.scheduled")
    ).alias("scheduled_arrival"),
)

# Data quality checks
quality_report = flights.select(
    count("*").alias("total_rows"),
    count(
        when(col("flight_iata").isNull(), 1)
    ).alias("missing_flight_iata"),
)

print("Data Quality Report:")
quality_report.show()

# Display results
print("Flight DataFrame schema:")
flights.printSchema()

print("First 10 flights:")
flights.show(10, truncate=False)

print(f"Total flights: {flights.count()}")

# Save transformed data in Parquet format
output_path = "data/processed/flights"

flights.write \
    .mode("overwrite") \
    .parquet(output_path)

print(f"Data saved to: {output_path}")

spark.stop()
