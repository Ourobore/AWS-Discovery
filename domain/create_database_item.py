import json
import os

import boto3


def create_database_item(payload: dict):
    db = boto3.resource(
        "dynamodb",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_DEFAULT_REGION"),
    )
    table = db.Table(os.environ.get("AWS_DYNAMODB_TABLE"))
    table.put_item(Item=json.loads(json.dumps(payload, default=str)))
