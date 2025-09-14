import json
import os
from dataclasses import asdict

import boto3
from boto3.dynamodb.conditions import Key
from model.model import AlbumResponse

TABLE_NAME = os.environ['TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    album_id = event['pathParameters'].get("id")


    item = table.get_item(
        Key={'PK': f'ALBUM#{album_id}', "SK": "METADATA"},
    ).get("Item")

    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': "Album not found"}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        }

    track_records = item.get("Songs") or {}

    track_ids = list(track_records.keys())
    print(track_ids)
    response = AlbumResponse(
        id=album_id,
        tracks=track_ids
    )
    return {
        'statusCode': 200,
        'body': json.dumps(asdict(response)),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
    }
