import gzip
import csv
import os

from io import BytesIO
from utilities import (
    get_last_processed_line,
    update_last_processed_line,
    connect_to_s3,
    connect_to_postgres,
)

# PostgreSQL credentials and configuration
TITLE_BASICS_TABLE_NAME = os.environ.get("TITLE_BASICS_TABLE_NAME")


def process_data():
    s3 = connect_to_s3()
    conn = connect_to_postgres()
    cursor = conn.cursor()

    response = s3.get_object(
        Bucket=os.environ.get("S3_RAW_DATA_BUCKET_NAME"),
        Key=os.environ.get("S3_RAW_TITLE_BASICS_KEY"),
    )

    last_processed_line = get_last_processed_line(TITLE_BASICS_TABLE_NAME)
    row_count = 0

    with gzip.open(BytesIO(response["Body"].read()), "rt") as file:
        reader = csv.DictReader(file, delimiter="\t")

        # Skip already processed rows
        for row in reader:
            row_count += 1
            if row_count <= last_processed_line:
                continue

            if row["startYear"] == "\\N":
                row["startYear"] = None

            if not row["genres"]:
                row["genres"] = []  # Else it would be trying to list(Nonetype)

            cursor.execute(
                f"INSERT INTO {TITLE_BASICS_TABLE_NAME} (tconst, startYear, genres) VALUES (%s, %s,%s)",
                (
                    row["tconst"],
                    row["startYear"],
                    list(row["genres"]),
                ),
            )

            if row_count % 50000 == 0:
                conn.commit()
                update_last_processed_line(TITLE_BASICS_TABLE_NAME, row_count)

    conn.commit()
    update_last_processed_line(TITLE_BASICS_TABLE_NAME, row_count)
    cursor.close()
    conn.close()


if __name__ == "__main__":
    process_data()
