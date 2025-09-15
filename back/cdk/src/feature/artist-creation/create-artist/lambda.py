import json
import os
import uuid
from dataclasses import asdict
from datetime import datetime

import boto3
import requests
from jwt import PyJWKClient, decode
from error_handling import with_error_handling

from model.artist import Artist, GenreDTO


TABLE_NAME = os.environ['DYNAMO']
dynamo = boto3.resource('dynamodb')
table = dynamo.Table(TABLE_NAME)

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
@with_error_handling(["Admin"])
def lambda_handler(event, context):
    # claims = event['requestContext']['authorizer']['claims']
    # user_groups = claims.get("cognito:groups", [])
    #
    # if "Admin" not in user_groups:
    #     return {
    #         "statusCode": 403,
    #         "body": "User is not in Admin group"
    #     }
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
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps({"error": f"Genres not found: {missing}"})
        }

    artist_id = str(uuid.uuid4())

    item = Artist(
        PK = f'ARTIST#{artist_id}',
        Name=name,
        Biography=biography,
        CreatedAt=datetime.utcnow().isoformat(),
        Songs={},
        Genres=found_genres,
        Albums={},
        EntityType="ARTIST"
    )
    table.put_item(Item=asdict(item))

    artist_dto = {
        "id": artist_id,
        "name": name,
        "biography": biography
    }
    # invoke
    lambda_client = boto3.client("lambda")
    lambda_client.invoke(
        FunctionName=os.environ["UPDATE_GENRE_LAMBDA_NAME"],
        InvocationType="Event",  # asinhrono
        Payload=json.dumps({
            "artistDTO": artist_dto,
            "genres": genre_ids
        }),
    )

    return {
        "statusCode": 201,
        "headers": {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    },
        "body": json.dumps({"message": "Artist created", "genreId": artist_id, })
    }
