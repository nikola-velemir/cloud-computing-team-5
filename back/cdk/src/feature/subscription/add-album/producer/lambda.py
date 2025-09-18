import json
import os
import boto3
from boto3.dynamodb.types import TypeDeserializer

sqs = boto3.client('sqs')
deserializer = TypeDeserializer()

ARTIST_QUEUE_URL = os.environ["ARTIST_QUEUE_URL"]
GENRE_QUEUE_URL = os.environ["GENRE_QUEUE_URL"]

def lambda_handler(event, context):
    payload = event
    event_type = payload.get("type")

    if event_type not in ["ARTIST", "ALBUM", "SONG"]:
        return {"statusCode": 400, "body": f"Unsupported event type: {event_type}"}

    new_image = payload["dynamodb"]
    pk = new_image["PK"]["S"]

    album = {
        "id": pk.replace("ALBUM#", ""),
        "Name": new_image.get("Title", {}).get("S", ""),
        "CoverPath": new_image.get("CoverPath", {}).get("S", "")
    }

    genres = []
    if "Genres" in new_image:
        for g in new_image["Genres"]["M"].values():
            genres.append({k: deserializer.deserialize(v) for k, v in g["M"].items()})

    artists = []
    if "Artists" in new_image:
        for a in new_image["Artists"]["M"].values():
            artists.append({k: deserializer.deserialize(v) for k, v in a["M"].items()})

    sqs.send_message(
        QueueUrl=GENRE_QUEUE_URL,
        MessageBody=json.dumps({
            "type": "ALBUM",
            "genres": genres,
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

    return {"statusCode": 200, "body": f"Processed album {album['Name']}"}
