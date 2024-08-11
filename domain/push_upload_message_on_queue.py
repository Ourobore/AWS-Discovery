import json
import os

import boto3


def push_upload_message_on_queue(dynamodb_key: str, s3_key: str) -> dict:
    """Sends a message on the SQS queue with the `dynamodb_key` and `s3_key` in it."""
    sqs = boto3.client(
        "sqs",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_DEFAULT_REGION"),
    )
    queue_url = sqs.get_queue_url(QueueName=os.environ.get("AWS_SQS_UPLOAD_QUEUE"))["QueueUrl"]
    payload = {"dynamodb_key": dynamodb_key, "s3_key": s3_key}
    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(payload, default=str))

    return payload
