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
    for record in event["Records"]:
        if record["eventName"] != "INSERT":
            continue

        try:
            new_image = record["dynamodb"]["NewImage"]
            pk = new_image["PK"]["S"]
            if not pk.startswith("SONG#"):
                continue

            song = {
                "Id": pk.replace("SONG#", ""),
                "Name": new_image.get("Name", {}).get("S", "")
            }

            album = {k: deserializer.deserialize(v) for k, v in new_image.get("Album", {}).get("M", {}).items()} if "Album" in new_image else None

            genre = {k: deserializer.deserialize(v) for k, v in
                     new_image.get("Genre", {}).get("M", {}).items()} if "Genre" in new_image else None

            artists = []
            if "Artists" in new_image:
                for a in new_image["Artists"]["M"].values():
                    artists.append({k: deserializer.deserialize(v) for k, v in a["M"].items()})

            if album:
                print(album)
                sqs.send_message(
                    QueueUrl=ALBUM_QUEUE_URL,
                    MessageBody=json.dumps({
                        "type": "SONG",
                        "album": album,
                        "song": song,
                    })
                )


            sqs.send_message(
                QueueUrl=GENRE_QUEUE_URL,
                MessageBody=json.dumps({
                    "type": "SONG",
                    "genre": genre,
                    "song": song
                })
            )

            for artist in artists:
                sqs.send_message(
                    QueueUrl=ARTIST_QUEUE_URL,
                    MessageBody=json.dumps({
                        "type": "SONG",
                        "artist": artist,
                        "song": song
                    })
                )

            print(f"[INFO] Sent messages for song {song['Name']}")

        except Exception as e:
            print(f"[ERROR] {e}")
            continue

    return {"statusCode": 200, "body": "Messages sent"}
