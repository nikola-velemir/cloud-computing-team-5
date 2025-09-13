import json
import os
from dataclasses import asdict
from datetime import datetime

import boto3
import jwt

from model import *

TABLE_NAME = os.environ['TABLE_NAME']
table = boto3.resource('dynamodb').Table(TABLE_NAME)
REVIEW_TYPES = json.loads(os.environ['REVIEW_TYPES'])


def lambda_handler(event, context):
    headers = event.get("headers", {})
    auth_header = headers.get("Authorization")
    if not auth_header:
        return {"statusCode": 401, "body": "Missing Authorization header"}

    token = auth_header.split(" ")[1]

    # Decode JWT claims (without verifying signature)
    claims = jwt.decode(token, options={"verify_signature": False})
    print("JWT Claims:", claims)

    # Cognito user ID is usually in 'sub'
    user_id = claims.get("sub")

    body = json.loads(event.get("body") or {})
    print(body)

    artist_id = body.get("artistId")
    review_type = body.get("reviewType")
    if review_type == 'NONE':
        table.delete_item(
            Key={
                'User': f'USER#{user_id}',
                "Content": f'ARTIST#{artist_id}',
            })
        return {
            "statusCode": 200,
            "body": json.dumps({}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }

    table_item = table.get_item(Key={"User": f'USER#{user_id}', "Content": f'ARTIST#{artist_id}'}).get("Item")
    print(table_item)
    if table_item and table_item.get("Rating") == review_type:
        table.delete_item(
            Key={
                'User': f'USER#{user_id}',
                "Content": f'ARTIST#{artist_id}',
            })
    else:
        record = AlbumReviewRecord(
            User=f"USER#{user_id}",
            Content=f"ARTIST#{artist_id}",
            Rating=review_type,
            Timestamp=datetime.now().isoformat()
        )
        table.put_item(Item=asdict(record))
    return {
        "statusCode": 200,
        "body": json.dumps({}),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    }
