import json
import os
import boto3
from boto3.dynamodb.conditions import Key

from error_handling import with_error_handling

TABLE_NAME = os.environ.get("DYNAMO")
dynamo = boto3.resource("dynamodb")
table = dynamo.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Event primer:
    {
        "artist_id": "uuid-of-artist",
        "artist_name": "New Artist Name"
    }
    """
    artist_id = event.get("artist_id")
    artist_name = event.get("artist_name")

    if not artist_id or not artist_name:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "artist_id and artist_name are required"})
        }

    try:
        response = table.query(
            IndexName="ReviewContentIndex",
            KeyConditionExpression=Key('Content').eq(f'ARTIST#{artist_id}')
        )

        for item in response.get("Items", []):
            if item["Content"] == f'ARTIST#{artist_id}':
                item["NameEntity"] = artist_name
                table.put_item(Item=item)


        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Artist {artist_name} updated in subscriptions"})
        }

    except Exception as e:
        print("Error updating subscriptions:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
