import json
import os

import boto3
from boto3.dynamodb.types import TypeDeserializer

sqs = boto3.client('sqs')
deserializer = TypeDeserializer()

FEED_SQS_URL = os.environ['FEED_SQS_URL']

# Event Name: INSERT | MODIFY
# New Image:
#   PK: ALBUM#1234
#   SK: USER#5678
#   Rating: LIKE, DISLIKE, LOVE
def lambda_handler(event, context):
    for record in event['Records']:
        # INSERT, MODIFY, REMOVE
        oper = record['eventName']
        if oper == 'REMOVE':
            continue
        new_image = record['dynamodb']['NewImage']

        user_id = new_image.get("User", {}).get("S")
        content_id = new_image.get("Content", {}).get("S")
        rating = new_image.get("Rating", {}).get("S")

        body = {
            "user": user_id,
            "content": content_id,
            "rating": rating,
            "operation": oper,
            "imagePath": new_image.get("CoverPath", {}).get("S"),
            "name" : new_image.get("NameEntity", {}).get("S"),
        }
        sqs.send_message(
            QueueUrl=FEED_SQS_URL,
            MessageBody=json.dumps({
                "type" : "REVIEW",
                "body" : json.dumps(body)
            })
        )

        print(f"Review for {user_id} sent to feed sqs")