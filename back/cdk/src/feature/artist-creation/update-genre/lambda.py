import json
import os
import boto3
from datetime import datetime, timezone


# DynamoDB setup
TABLE_NAME = os.environ["DYNAMO"]
dynamo = boto3.resource("dynamodb")
table = dynamo.Table(TABLE_NAME)


def lambda_handler(event, context):
    """
    Event primer:
    {
        "artistDTO": {
            "id": "uuid",
            "name": "Artist name",
            "biography": "Artist biography"
        },
        "genres": [1, 2, 3]
    }
    """

    print("Received event:", json.dumps(event))

    artist_dto = event.get("artistDTO")
    genre_ids = event.get("genres", [])

    if not artist_dto or not genre_ids:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"error": "Missing artistDTO or genres list"}
            ),
        }

    artist_id = artist_dto.get("id")
    if not artist_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "artistDTO.id is required"}),
        }
    for gid in genre_ids:
        try:
            pk = f"GENRE#{gid}"
            sk = "METADATA"
            now_iso = datetime.now(timezone.utc).isoformat()

            resp = table.get_item(Key={"PK": pk, "SK": sk})
            existing = resp.get("Item", {}).get("Artists", {})

            existing[artist_id] = artist_dto

            table.update_item(
                Key={"PK": pk, "SK": sk},
                UpdateExpression="SET Artists = :artists, UpdatedAt = :updatedAt",
                ExpressionAttributeValues={
                    ":artists": existing,
                    ":updatedAt": now_iso
                },
            )
            print(f"Genre {gid} updated with artist {artist_id}")
        except Exception as e:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Updating genre"}),
            }


    print("Finished updating genres list")

