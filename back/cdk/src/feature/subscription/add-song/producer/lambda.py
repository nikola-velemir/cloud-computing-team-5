import json
import os
import boto3
from boto3.dynamodb.types import TypeDeserializer

sqs = boto3.client('sqs')
deserializer = TypeDeserializer()

ALBUM_QUEUE_URL = os.environ["ALBUM_QUEUE_URL"]
ARTIST_QUEUE_URL = os.environ["ARTIST_QUEUE_URL"]
GENRE_QUEUE_URL = os.environ["GENRE_QUEUE_URL"]

def lambda_handler(event, context):
    payload = event
    event_type = payload.get("type")

    if event_type not in ["ARTIST", "ALBUM", "SONG"]:
        return {"statusCode": 400, "body": f"Unsupported event type: {event_type}"}

    new_image = payload["dynamodb"]
    pk = new_image["PK"]["S"]

    song = {
        "Id": pk.replace("SONG#", ""),
        "Name": new_image.get("Name", {}).get("S", "")
    }

    album = {k: deserializer.deserialize(v) for k, v in new_image.get("Album", {}).get("M", {}).items()} if "Album" in new_image else None
    genre = {k: deserializer.deserialize(v) for k, v in new_image.get("Genre", {}).get("M", {}).items()} if "Genre" in new_image else None

    artists = []
    if "Artists" in new_image:
        for a in new_image["Artists"]["M"].values():
            artists.append({k: deserializer.deserialize(v) for k, v in a["M"].items()})

    # Slanje poruka u odgovarajuće SQS
    if album:
        sqs.send_message(
            QueueUrl=ALBUM_QUEUE_URL,
            MessageBody=json.dumps({"type": "SONG", "album": album, "song": song})
        )

    if genre:
        sqs.send_message(
            QueueUrl=GENRE_QUEUE_URL,
            MessageBody=json.dumps({"type": "SONG", "genre": genre, "song": song})
        )

    for artist in artists:
        sqs.send_message(
            QueueUrl=ARTIST_QUEUE_URL,
            MessageBody=json.dumps({"type": "SONG", "artist": artist, "song": song})
        )

    print(f"[INFO] Sent messages for song {song['Name']}")
    return {"statusCode": 200, "body": f"Processed song {song['Name']}"}
