import json
import os

from model.genre import Genre
import boto3
from dataclasses import asdict

TABLE_NAME = os.environ['DYNAMO']
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)
s3_client = boto3.client("s3")
BUCKET_NAME = os.environ['BUCKET']
EXPIRATION_TIME = int(os.environ['EXPIRATION_TIME'])


def lambda_handler(event, context):
    db_response = table.scan(
        FilterExpression="begins_with(PK, :genre)",
        ExpressionAttributeValues={
            ":genre": "GENRE#"
        }
    )
    items = db_response.get("Items", [])

    responses = [
        asdict(Genre(id=item["PK"].split("#")[1],
                     name=item.get("Name"),
                     url=_get_cover_url(item["PK"].split("#")[1]))
               ) for item in items]

    return {
        'statusCode': 200,
        'body': json.dumps(responses),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    }

def _get_cover_url(genre_id: str):
    key = f'{genre_id}/image/image.ico'
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": key},
            ExpiresIn = EXPIRATION_TIME
        )
    except Exception as e:
        print("Error:", e)
        return None
