import json
import os

import boto3
from boto3.dynamodb.types import TypeDeserializer

sqs = boto3.client('sqs')
deserializer = TypeDeserializer()

GENRE_QUEUE_URL = os.environ["GENRE_QUEUE_URL"]

# what triggers when artist ws created
def lambda_handler(event, context):
    for record in event["Records"]:
        if record["eventName"] == "INSERT":
            continue
        try:
            new_image = record["dynamodb"]["NewImage"]
            pk = new_image["PK"]["S"]
            if not pk.startswith("ARTIST#"):
                continue

            artist = {
                "id": pk.replace("ARTIST#", ""),
                "Name": new_image.get("Name", {}).get("S", ""),
            }

            genre = {k: deserializer.deserialize(v) for k, v in
                     new_image.get("Genre", {}).get("M", {}).items()} if "Genre" in new_image else None


            sqs.send_message(
                QueueUrl=GENRE_QUEUE_URL,
                MessageBody=json.dumps({
                    "type": "ARTIST",
                    "genre": genre,
                    "artist": artist
                })
            )


            print(f"[INFO] Sent messages for artist {artist['Name']}")


        except Exception as e:
            print(e)
            continue
