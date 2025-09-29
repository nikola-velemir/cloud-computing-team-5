import json
import os
import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = os.environ['DYNAMO']
dynamo = boto3.resource('dynamodb')
table = dynamo.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Event primer:
    {
        "artist_id": "uuid-of-artist",
        "genre_ids": ["genre_id_1", "genre_id_2", ...]
    }
    """
    artist_id = event.get("artist_id")
    genre_ids = event.get("genre_ids", [])

    if not artist_id or not genre_ids:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "artist_id and genre_ids are required"})
        }

    try:
        for genre_id in genre_ids:
            response = table.query(
                KeyConditionExpression=Key("PK").eq(f"GENRE#{genre_id}") & Key("SK").eq("METADATA")
            )

            for item in response.get("Items", []):
                if "Artists" in item:
                    item["Artists"].pop(artist_id)
                    table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Artist removed from genres"})
        }

    except Exception as e:
        print("Error removing artist from genres:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
