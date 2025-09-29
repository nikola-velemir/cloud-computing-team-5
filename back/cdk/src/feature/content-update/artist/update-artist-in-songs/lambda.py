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
        "artist_name": "New Artist Name",
        "song_ids": ["song_id_1", "song_id_2", ...]
    }
    """
    artist_id = event.get("artist_id")
    artist_name = event.get("artist_name")
    song_ids = event.get("song_ids", [])

    if not artist_id or not artist_name or not song_ids:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "artist_id, artist_name, and song_ids are required"})
        }

    try:
        for song_id in song_ids:
            response = table.query(
                KeyConditionExpression=Key("PK").eq(f"SONG#{song_id}") & Key("SK").eq("METADATA")
            )

            for item in response.get("Items", []):
                if "Artists" in item:
                    item["Artists"][artist_id]["Name"] = artist_name
                    table.put_item(Item=item)
                    break

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Artist {artist_name} updated in songs"})
        }

    except Exception as e:
        print("Error updating songs:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
