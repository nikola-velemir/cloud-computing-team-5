import json
import os

import boto3
from boto3.dynamodb.types import TypeDeserializer

sqs = boto3.client('sqs')
deserializer = TypeDeserializer()

ARTIST_QUEUE_URL = os.environ["ARTIST_QUEUE_URL"]
GENRE_QUEUE_URL = os.environ["GENRE_QUEUE_URL"]

# what triggers when album ws created
def lambda_handler(event, context):
    for record in event["Records"]:
        if record["eventName"] == "INSERT":
            continue
        try:
            new_image = record["dynamodb"]["NewImage"]
            pk = new_image["PK"]["S"]
            if not pk.startswith("ALBUM#"):
                continue

            album = {
                "id": pk.replace("ALBUM#", ""),
                "Name": new_image.get("Title", {}).get("S", ""),
            }

            genre = {k: deserializer.deserialize(v) for k, v in
                     new_image.get("Genre", {}).get("M", {}).items()} if "Genre" in new_image else None

            artists = []
            if "Artists" in new_image:
                for a in new_image["Artists"]["M"].values():
                    artists.append({k: deserializer.deserialize(v) for k, v in a["M"].items()})

            sqs.send_message(
                QueueUrl=GENRE_QUEUE_URL,
                MessageBody=json.dumps({
                    "type": "ALBUM",
                    "genre": genre,
                    "album": album
                })
            )
            for artist in artists:
                sqs.send_message(
                    QueueUrl=ARTIST_QUEUE_URL,
                    MessageBody=json.dumps({
                        "type": "ALBUM",
                        "artist": artist,
                        "album": album
                    })
                )

            print(f"[INFO] Sent messages for album {album['Title']}")


        except Exception as e:
            print(e)
            continue
