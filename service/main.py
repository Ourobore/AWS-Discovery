import dotenv
import boto3
import os
import datetime
import json

dotenv.load_dotenv()


def main():
    credentials = {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY"),
        "region_name": os.environ.get("AWS_DEFAULT_REGION"),
    }
    sqs = boto3.client("sqs", **credentials)
    queue_url = sqs.get_queue_url(QueueName=os.environ.get("AWS_SQS_UPDATE_QUEUE"))["QueueUrl"]

    db = boto3.resource("dynamodb", **credentials)
    table = db.Table(os.environ.get("AWS_DYNAMODB_TABLE"))

    s3 = boto3.resource("s3", **credentials)
    bucket = s3.Bucket(os.environ.get("AWS_S3_BUCKET"))

    while 1:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20,
        )

        messages = response.get("Messages")
        if not messages:
            continue

        message = messages[0]
        receipt_handle = message["ReceiptHandle"]
        dynamodb_key, s3_key = json.loads(message["Body"]).values()

        bucket.download_file(Key=s3_key, Filename="s3_" + s3_key)
        laptop_item = table.get_item(Key={"uuid": dynamodb_key})["Item"]
        print(laptop_item)

        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)


if __name__ == "__main__":
    main()
