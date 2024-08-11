import json
from datetime import datetime

import boto3


def lambda_handler(event, context):
    db = boto3.resource("dynamodb")
    table = db.Table("laptops")

    timestamp = datetime.now()
    dynamodb_key, s3_key = json.loads(event["Records"][0]["body"]).values()
    table.update_item(
        Key={"uuid": dynamodb_key},
        UpdateExpression="SET #timestamp = :ts",
        ExpressionAttributeNames={"#timestamp": "timestamp"},
        ExpressionAttributeValues={":ts": str(timestamp)},
    )

    sqs = boto3.client("sqs")
    queue_url = sqs.get_queue_url(QueueName="updated-laptops")["QueueUrl"]
    payload = {"dynamodb_key": dynamodb_key, "s3_key": s3_key}
    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(payload, default=str))

    return {"statusCode": 200, "body": json.dumps(f"Updated DynamoDB key {dynamodb_key}: timestamp set to {timestamp}")}
