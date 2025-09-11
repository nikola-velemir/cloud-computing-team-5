import json
import os
import uuid
from dataclasses import asdict
from datetime import datetime

import boto3
import requests
from jwt import PyJWKClient, decode

from model.artist import Artist, GenreDTO


TABLE_NAME = os.environ['DYNAMO']
dynamo = boto3.resource('dynamodb')
table = dynamo.Table(TABLE_NAME)

COGNITO_POOL_ID = 'eu-central-1_TTH9eq5eX'
COGNITO_REGION = 'eu-central-1'
CLIENT_ID = '2bhb4d2keh19gbj25tuild6ti1'
JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_POOL_ID}/.well-known/jwks.json"

JWKS = requests.get(JWKS_URL).json()

def verify_user_groups(headers: dict, allowed_groups: list):
    auth_header = headers.get("Authorization", "")
    if not auth_header:
        raise Exception("Missing Authorization header")

    token = auth_header.replace("Bearer ", "")
    jwk_client = PyJWKClient(JWKS_URL)
    signing_key = jwk_client.get_signing_key_from_jwt(token)

    try:

        decoded = decode(
            token,
            key=signing_key.key,
            algorithms=["RS256"],
            audience=CLIENT_ID
        )

        user_groups = decoded.get("cognito:groups", [])
        if not any(group in allowed_groups for group in user_groups):
            raise Exception("User not authorized")
        return decoded
    except Exception as e:
        raise Exception(f"Authorization failed: {str(e)}")

def with_error_handling(handler):
    def wrapper(event, context):
        try:
            return handler(event, context)
        except Exception as e:
            return {
                "statusCode": 403,
                "body": str(e)
            }
    return wrapper

def _map_genre_to_dto(item):
    return GenreDTO(
        Id=item['PK'].replace("GENRE#", ""),
        Name=item['Name'],
        Image=item['CoverPath'],
    )

# body : {
#   "name" : "artist name",
#   "biography" : "my bio",
#   "genres_id" : [1,2,3],
#   "albums_id" : [1,2,3], -optional
#   "songs_id" : [1,2,3], -optional
# }
# @with_error_handling
def lambda_handler(event, context):
    # decoded_token = verify_user_groups(event['headers'], ["ADMIN"])
    if "body" in event:
        body = json.loads(event["body"])
    else:
        body = event
    genre_ids = body['genres_id']
    name = body['name']
    biography = body['biography']

    if not genre_ids:
        return {"statusCode": 400, "body": json.dumps({"error": "No genres provided"})}

    if not name:
        return {"statusCode": 400, "body": json.dumps({"error": "No name provided"})}

    if not biography:
        return {"statusCode": 400, "body": json.dumps({"error": "No biography provided"})}

    keys = [{'PK': f'GENRE#{gid}', 'SK': "METADATA"} for gid in genre_ids]
    resp = dynamo.meta.client.batch_get_item(
        RequestItems={
            TABLE_NAME : {"Keys": keys},
        }
    )
    found_items = resp["Responses"].get(TABLE_NAME, [])
    found_genres = []
    for item in found_items:
        found_genres.append(_map_genre_to_dto(item))

    print(found_genres)
    found_ids = {item["PK"].replace("GENRE#", "") for item in found_items}

    missing = [gid for gid in genre_ids if str(gid) not in found_ids]
    if missing:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Genres not found: {missing}"})
        }

    artist_id = str(uuid.uuid4())

    item = Artist(
        PK = f'ARTIST#{artist_id}',
        Name=name,
        Biography=biography,
        UpdatedAt=datetime.utcnow().isoformat(),
        Songs={},
        Genres={},
        Albums={}
    )
    table.put_item(Item=asdict(item))

    return {
        "statusCode": 201,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"message": "Artist created", "genreId": artist_id, })
    }
