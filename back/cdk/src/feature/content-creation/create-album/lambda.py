import json
import os
import uuid
from dataclasses import asdict

from model.album import Album

import boto3

TABLE_NAME = os.environ['TABLE_NAME']
dynamo = boto3.resource('dynamodb')
table = dynamo.Table(TABLE_NAME)


def lambda_handler(event, context):
    event_body = json.loads(event['body'])
    album_id = str(uuid.uuid4())
    album = Album(
        Id= album_id,
        GenreId= event_body['genreId'],
        Title= event_body['title'],
    )
    dynamo.put_item(Item=asdict(album))
    return {
        'statusCode': 201,
        'body': json.dumps({'albumId': album_id}),
    }
