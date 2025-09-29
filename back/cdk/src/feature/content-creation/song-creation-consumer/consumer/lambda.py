import os
import boto3
import json

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO"])


def lambda_handler(event, _context):
    for record in event["Records"]:
        try:
            body = json.loads(record["body"])

            if body.get("type") != "SONG_CREATED":
                continue

            song_id = body["song_id"]
            song_data = {
                "Id": song_id,
                "Name": body["name"],
                "CoverPath": body["cover_path"],
                "AudioPath": body["audio_path"],
                "ReleaseDate": body["release_date"],
                "Duration": int(body["duration"]),
                "GenreId": body["genre_id"],
                "EntityType": "SONG"
            }

            # --- Update Genre ---
            if body.get("genre_id"):
                table.update_item(
                    Key={"PK": f"GENRE#{body['genre_id']}", "SK": "METADATA"},
                    UpdateExpression="SET #songs.#song_id = :song",
                    ExpressionAttributeNames={
                        "#songs": "Songs",
                        "#song_id": song_id,
                    },
                    ExpressionAttributeValues={":song": song_data},
                )
            album_id = body.get("album_id")
            if album_id:

                table.update_item(
                    Key={"PK": f"ALBUM#{album_id}", "SK": "METADATA"},
                    UpdateExpression="SET #songs.#song_id = :song",
                    ExpressionAttributeNames={
                        "#songs": "Songs",
                        "#song_id": song_id,
                    },
                    ExpressionAttributeValues={":song": song_data},
                    ReturnValues="UPDATED_NEW"
                )
            # --- Update Artists ---
            for artist_id in body.get("artist_ids", []):
                table.update_item(
                    Key={"PK": f"ARTIST#{artist_id}", "SK": "METADATA"},
                    UpdateExpression="SET #songs.#song_id = :song",
                    ExpressionAttributeNames={
                        "#songs": "Songs",
                        "#song_id": song_id,
                    },
                    ExpressionAttributeValues={":song": song_data},
                )

        except Exception as e:
            print("Error processing record:", e)
            continue
