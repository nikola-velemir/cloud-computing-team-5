import json
import os
import uuid
import base64
from dataclasses import asdict
from datetime import datetime

import boto3
from model.genre import Genre

TABLE_NAME = os.environ.get("DYNAMO")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, _context):
    headers = event.get('headers') or {}
    content_type = headers.get('content-type') or headers.get('Content-Type')
    if not content_type:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Missing Content-Type header"})
        }
    body = json.loads(event['body'])
    genre_id = str(uuid.uuid4())
    image_type = body.get('imageType').split('/')[-1]

    cover_path = f'{genre_id}/cover/cover.{image_type}' if image_type else '';
    item = Genre(
        PK=f'GENRE#{genre_id}',
        Description=body.get('description') or '',
        Name=body.get('name') or '',
        Songs={},
        Albums={},
        UpdatedAt=datetime.utcnow().isoformat(),
        CoverPath=cover_path
    )
    table.put_item(Item=asdict(item))
    return {
        "statusCode": 201,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"message": "Genre created", "genreId": genre_id, })
    }
