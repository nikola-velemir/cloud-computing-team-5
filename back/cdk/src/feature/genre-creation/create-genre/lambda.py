import json
import os
import uuid
import base64
from dataclasses import asdict
import boto3
from model.genre import Genre

TABLE_NAME = os.environ.get("DYNAMO")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    headers = event.get('headers') or {}
    content_type = headers.get('content-type') or headers.get('Content-Type')
    if not content_type:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Missing Content-Type header"})
        }
    body = json.loads(event['body'])
    genre_id = str(uuid.uuid4())
    item = Genre(
        PK=f'GENRE#{genre_id}',
        SK='METADATA',
        Description=body['description'],
        Name=body['name'],
    )
    table.put_item(Item=asdict(item))
    return {
        "statusCode": 201,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"message": "Genre created", "genreId": genre_id,})
    }