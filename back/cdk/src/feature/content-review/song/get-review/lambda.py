import json
import os
from dataclasses import asdict
from datetime import datetime
from  model import  *
import boto3
import jwt

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
    path_params = event.get('pathParameters') or {}

    song_id = path_params.get('id')

    item = table.get_item(Key={"User": f'USER#{user_id}', "Content": f'SONG#{song_id}'}).get("Item")
    response = SongReviewResponse(
        reviewType= "NONE" if not item else item.get("Rating")
    )

    return {
        "statusCode": 200,
        "body": json.dumps(asdict(response)),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    }
