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
