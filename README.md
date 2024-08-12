# AWS Discovery

The goal of this project was to discover the [AWS](https://aws.amazon.com/) ecosystem and it's services, as well as gaining new skills.

## Architecture

- A Python script that will:
  - Create a JSON file with a few key value pairs
  - Upload said file to a [S3](https://aws.amazon.com/s3/) bucket
  - Store these key value pairs inside a [DynamoDB](https://aws.amazon.com/dynamodb/) table
  - Send a message on a [SQS](https://aws.amazon.com/sqs/) queue with the corresponding bucket and database item keys
- Messages in said queue will trigger a [Lambda](https://aws.amazon.com/lambda/):
  - This Lambda will modify the item corresponding to the key from the message
  - It will also send a message on a second SQS queue, with the same couple of keys
- And finally a Python service listening on this second SQS queue:
  - With the keys in the message, it will fetch both the database item and the file in the bucket

The idea here is that the original and final files are the same, but the original and final state are not.

## Infrastructure configuration

This repository doesn't contain any infrastructure definition via [CDK](https://aws.amazon.com/cdk/). So for the logic included in this repository to work correctly, be sure to already have deployed the necessary AWS services and configuration. This include:

- **DynamoDB** - A database table to store key value pairs
- **S3** - A storage bucket to store JSON files
- **SQS** - 3 messages queues
  - The first one for the script to upload messages and the Lambda to reads them
  - The second one for the Lambda to upload messages and the service to read them
  - A third one that's is a Dead Letter Queue for the second one for messages that were not correctly read by the service
- **Lambda** - Some logic that reads the first queue, update the database table, and push messages on the second queue. The logic corresponds to the `adapters/update_database_item_lambda.py` file
- **IAM** - Non root user with access keys to not use the root credentials
  -  Minimal policies needed regrouped into a group linked to this user
     -  For the script:
        -  Write access on the DynamoDB table to create item
        -  Write access on the S3 bucket to upload file
        -  Write access on the first SQS queue to push message
     -  For the service:
        -  Read access on the second SQS queue to receive messages
        -  Read access on the DynamoDB table to get item
        -  Read access on the S3 bucket to download file
-  **IAM** - Minimal policies needed by the Lambda logic
   -  Read access on the first SQS queue to receive messages
   -  Write access on the DynamoDB table to update an item
   -  Write access on the second SQS queue to push pessages

## How to run it

This project uses [Poetry](https://python-poetry.org/) as it's dependency manager. So to install the project, you can run the following command:
``` bash
poetry install
```

Also, don't forget to copy the `example.env` file into a `.env` file, and fill in the missing values.

Then, you can start the service that will listen to the second SQS queue.
``` bash
python service/main.py
```

And finally, you can run the script that will create the JSON file, store the value and file, and push a message on the first queue, by giving the command the desired filename.
``` bash
python scripts/generate_json_and_save_to_db_and_storage.py laptop.json
```
