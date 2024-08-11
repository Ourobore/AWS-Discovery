import os

import boto3


def upload_file_to_storage(filename: str):
    """Uploads file corresponding to `filename` to S3 storage"""
    s3 = boto3.resource(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_DEFAULT_REGION"),
    )
    bucket = s3.Bucket(os.environ.get("AWS_S3_BUCKET"))
    bucket.upload_file(filename, Key=filename)
