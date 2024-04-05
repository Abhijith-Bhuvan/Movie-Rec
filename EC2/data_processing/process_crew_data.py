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

CREW_TABLE_NAME = os.environ.get("TITLE_CREW_TABLE_NAME")


def process_crew_data():
    s3 = connect_to_s3()
    conn = connect_to_postgres()
    cursor = conn.cursor()

    response = s3.get_object(
        Bucket=os.environ.get("S3_RAW_DATA_BUCKET_NAME"),
        Key=os.environ.get("S3_RAW_TITLE_CREW_KEY"),
    )

    last_processed_line = get_last_processed_line(CREW_TABLE_NAME)
    row_count = 0

    with gzip.open(BytesIO(response["Body"].read()), "rt") as file:
        reader = csv.DictReader(file, delimiter="\t")

        for row in reader:

            # Skip already processed rows
            row_count += 1
            if row_count <= last_processed_line:
                continue

            if row["directors"] != "\\N" and row["writers"] != "\\N":
                row["directors"] = (
                    {row["directors"]}
                    if isinstance(row["directors"], str)
                    else row["directors"]
                )
                row["writers"] = (
                    {row["writers"]}
                    if isinstance(row["writers"], str)
                    else row["writers"]
                )

                cursor.execute(
                    f"SELECT tconst FROM {CREW_TABLE_NAME} WHERE tconst = %s",
                    (row["tconst"],),
                )
                existing_row = cursor.fetchone()

                if not existing_row:
                    cursor.execute(
                        f"INSERT INTO {CREW_TABLE_NAME} (tconst, directors, writers) VALUES (%s, %s, %s)",
                        (
                            row["tconst"],
                            list(row["directors"]),
                            list(row["writers"]),
                        ),
                    )

            if row_count % 50000 == 0:
                conn.commit()
                update_last_processed_line(CREW_TABLE_NAME, row_count)

    conn.commit()
    update_last_processed_line(CREW_TABLE_NAME, row_count)
    cursor.close()
    conn.close()


if __name__ == "__main__":
    process_crew_data()
