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

TITLE_AKAS_TABLE_NAME = os.environ.get("TITLE_AKAS_TABLE_NAME")


def process_data():
    s3 = connect_to_s3()
    conn = connect_to_postgres()
    cursor = conn.cursor()

    response = s3.get_object(
        Bucket=os.environ.get("S3_RAW_DATA_BUCKET_NAME"),
        Key=os.environ.get("S3_RAW_TITLE_AKAS_KEY"),
    )

    last_processed_line = get_last_processed_line(TITLE_AKAS_TABLE_NAME)
    row_count = 0

    with gzip.open(BytesIO(response["Body"].read()), "rt") as file:
        reader = csv.DictReader(file, delimiter="\t", quoting=csv.QUOTE_NONE)

        # Skip already processed rows
        for row in reader:
            row_count += 1
            if row_count <= last_processed_line:
                continue

            if len(row["title"]) > 255:
                # the column is VARCHAR(255)
                # it could be increased in the db but this is only triggred < 20 times
                # felt it was not worth it
                continue

            if not (
                (row["isOriginalTitle"] == 1) | (row["isOriginalTitle"] == "1")
            ):
                continue

            cursor.execute(
                f"SELECT titleId FROM {TITLE_AKAS_TABLE_NAME} WHERE titleId = %s",
                (row["titleId"],),
            )
            existing_row = cursor.fetchone()

            if not existing_row:
                cursor.execute(
                    f"INSERT INTO {TITLE_AKAS_TABLE_NAME} (title, titleId) VALUES (%s, %s)",
                    (
                        row["title"],
                        row["titleId"],
                    ),
                )

            if row_count % 50000 == 0:
                conn.commit()
                update_last_processed_line(TITLE_AKAS_TABLE_NAME, row_count)

    conn.commit()
    update_last_processed_line(TITLE_AKAS_TABLE_NAME, row_count)
    cursor.close()
    conn.close()


if __name__ == "__main__":
    process_data()
