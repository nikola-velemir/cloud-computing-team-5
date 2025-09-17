import json
import os

import boto3
from boto3.dynamodb.types import TypeDeserializer

sqs = boto3.client('sqs')
deserializer = TypeDeserializer()

FEED_SQS_URL = os.environ['FEED_SQS_URL']

def lambda_handler(event, context):
    for record in event['Records']:
        oper = record['eventName']
        if oper != "INSERT" and oper != "REMOVE":
            continue
        print(f"Received {record} event")
        if oper == "INSERT":
            new_image = record['dynamodb']['NewImage']
            item = {k: deserializer.deserialize(v) for k, v in new_image.items()}
        else:
            old_image = record['dynamodb']['OldImage']
            item = {k: deserializer.deserialize(v) for k, v in old_image.items()}

        entity = item["PK"]
        user = item["SK"]

        subscription_event = {
            "user": user,
            "content": entity,
            "name": item.get("Name"),
            "email": item.get("Email"),
            "operation": oper
        }
        sqs.send_message(
            QueueUrl=FEED_SQS_URL,
            MessageBody=json.dumps({
                "type": "SUBSCRIBE",
                "body": json.dumps(subscription_event)
            })
        )

        print(f"Subscribe to {entity} sent to feed sqs")