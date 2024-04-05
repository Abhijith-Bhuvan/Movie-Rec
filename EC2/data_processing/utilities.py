import os


# Fet the last processed line number from a marker file
def get_last_processed_line(table_name):
    try:
        with open(f"last_processed_line_{table_name}.txt", "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0


# Update the last processed line number in the marker file
def update_last_processed_line(table_name, line_number):
    with open(f"last_processed_line_{table_name}.txt", "w") as f:
        f.write(str(line_number))


def connect_to_s3():
    import boto3

    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def connect_to_postgres():
    import psycopg2

    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")

    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )
