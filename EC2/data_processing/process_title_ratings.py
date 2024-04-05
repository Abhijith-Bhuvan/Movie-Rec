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
TITLE_RATINGS_TABLE_NAME = os.environ.get("TITLE_RATINGS_TABLE_NAME")


def process_data():
    s3 = connect_to_s3()
    conn = connect_to_postgres()
    cursor = conn.cursor()

    response = s3.get_object(
        Bucket=os.environ.get("S3_RAW_DATA_BUCKET_NAME"),
        Key=os.environ.get("S3_RAW_TITLE_RATINGS_KEY"),
    )

    last_processed_line = get_last_processed_line(TITLE_RATINGS_TABLE_NAME)
    row_count = 0

    with gzip.open(BytesIO(response["Body"].read()), "rt") as file:
        reader = csv.DictReader(file, delimiter="\t")
        for row in reader:

            # Skip already processed rows
            row_count += 1
            if row_count <= last_processed_line:
                continue

            cursor.execute(
                f"INSERT INTO {TITLE_RATINGS_TABLE_NAME} (tconst, numvotes, aggregated_ratings) VALUES (%s, %s,%s)",
                (
                    row["tconst"],
                    row["numvotes"],
                    row["averageRating"],
                ),
            )

            if row_count % 50000 == 0:
                conn.commit()
                update_last_processed_line(TITLE_RATINGS_TABLE_NAME, row_count)

    conn.commit()
    update_last_processed_line(TITLE_RATINGS_TABLE_NAME, row_count)
    cursor.close()
    conn.close()


if __name__ == "__main__":
    process_data()
