import psycopg2
import redis

import os


def connect_postgres():

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


def connect_redis():
    host = os.environ.get("REDIS_HOST")
    r = redis.Redis(host=host, port=6379, decode_responses=True)
    return r


def fix_genres(input_str):
    """
    Genres data is messed up, the input looks like this:
        {'C,r,i,m,e,",",D,r,a,m,a'}
    Output should look like this:
        ["Crime","Drama"]

    Empty genres are represented by "\\N"
    So that is handled separately.
    """
    if input_str == "\\N":
        return []
    # Remove curly braces and single quotes
    cleaned_string = input_str[1:-1]

    # Split by ',",'
    substrings = cleaned_string.split(',"')

    genres = []
    for substring in substrings:
        # Remove commas from the substring
        genre = substring.replace(",", "")

        # Check if the string is not empty
        if genre:
            genres.append(genre)

    return genres
