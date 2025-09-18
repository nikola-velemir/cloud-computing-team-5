import json
import os

import boto3
from boto3.dynamodb.types import TypeDeserializer

sqs = boto3.client('sqs')
deserializer = TypeDeserializer()

GENRE_QUEUE_URL = os.environ["GENRE_QUEUE_URL"]

# what triggers when artist was created
def lambda_handler(event, context):
    payload = event
    event_type = payload.get("type")

    if event_type not in ["ARTIST", "ALBUM", "SONG"]:
        return {"statusCode": 400, "body": f"Unsupported event type: {event_type}"}

    new_image = payload["dynamodb"]
    pk = new_image["PK"]["S"]

    artist = {
        "id": pk.replace("ARTIST#", ""),
        "Name": new_image.get("Name", {}).get("S", ""),
        "CoverPath": new_image.get("CoverPath", {}).get("S", "")
    }

    genres = []
    if "Genres" in new_image:
        raw_genres = new_image["Genres"].get("L", [])
        genres = [
            {k: deserializer.deserialize(v) for k, v in g["M"].items()}
            for g in raw_genres
        ]

    sqs.send_message(
        QueueUrl=GENRE_QUEUE_URL,
        MessageBody=json.dumps({
            "type": "ARTIST",
            "genres": genres,
            "artist": artist
        })
    )


    print(f"[INFO] Sent messages for artist {artist['Name']}")

