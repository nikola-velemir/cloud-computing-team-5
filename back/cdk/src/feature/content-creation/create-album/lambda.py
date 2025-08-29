import json
import os
import uuid
from dataclasses import asdict

from model.album import Album

import boto3

TABLE_NAME = os.environ['DYNAMO']
dynamo = boto3.resource('dynamodb')
table = dynamo.Table(TABLE_NAME)


def lambda_handler(event, context):
    event_body = json.loads(event['body'])
    album_id = str(uuid.uuid4())
    album = Album(
        PK='ALBUM#' + album_id,
        GenreIds=event_body['genreIds'],
        Title=event_body['title'],
        ArtistIds=event_body['artistIds'],
    )
    table.put_item(Item=asdict(album))
    return {
        'statusCode': 201,
        'body': json.dumps({'albumId': album_id}),
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
    }
