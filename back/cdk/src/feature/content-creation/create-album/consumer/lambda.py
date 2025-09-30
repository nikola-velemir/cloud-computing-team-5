import os
import boto3
import json

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMO"])

def lambda_handler(event, _context):
    for record in event["Records"]:
        try:
            body = json.loads(record["body"])

            if body.get("type") != "ALBUM_CREATED":
                continue

            album_id = body["album_id"]
            album_ref = {
                "Id": album_id,
                "Title": body["title"],
                "ReleaseDate": body["release_date"],
                "CoverPath": body["cover_path"],
            }

            # --- Update Artists ---
            for artist_id in body.get("artist_ids", []):
                table.update_item(
                    Key={"PK": f"ARTIST#{artist_id}", "SK": "METADATA"},
                    UpdateExpression="SET #albums.#album_id = :album",
                    ExpressionAttributeNames={
                        "#albums": "Albums",
                        "#album_id": album_id,
                    },
                    ExpressionAttributeValues={":album": album_ref},
                )

            # --- Update Genres ---
            for genre_id in body.get("genre_ids", []):
                table.update_item(
                    Key={"PK": f"GENRE#{genre_id}", "SK": "METADATA"},
                    UpdateExpression="SET #albums.#album_id = :album",
                    ExpressionAttributeNames={
                        "#albums": "Albums",
                        "#album_id": album_id,
                    },
                    ExpressionAttributeValues={":album": album_ref},
                )

        except Exception as e:
            print("Error processing record:", e)
            continue
