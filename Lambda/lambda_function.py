import boto3
import os
import requests
import json

# sample curl statement
# curl -X POST https://testsample.execute-api.ap-south-1.amazonaws.com/test1/Raw_data \
#   -H 'content-type: application/json' \
#   -d '{ "s3_object_key": "name_basics_imdb", "url": "https://datasets.imdbws.com/name.basics.tsv.gz" }'


def lambda_handler(event, context):
    s3 = boto3.client("s3")
    s3_bucket_name = os.environ.get("S3_RAW_DATA_BUCKET_NAME")

    body = json.loads(event["body"])
    s3_object_name = body["s3_object_key"]
    imdb_tsv_url = body["url"]

    response = requests.get(imdb_tsv_url, stream=True)
    if response.status_code == 200:
        s3.upload_fileobj(response.raw, s3_bucket_name, s3_object_name)
        print(f"File uploaded to {s3_bucket_name}/{s3_object_name}")
    else:
        print(f"Failed to download file from {imdb_tsv_url}")
