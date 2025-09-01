import json
import os
from dataclasses import asdict

import boto3
from boto3.dynamodb.conditions import Key
from model.model import AlbumResponse

TABLE_NAME = os.environ['TABLE_NAME']
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    album_id = event['pathParameters'].get("id")
    if not album_id:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': "Album id is mandatory"}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        }

    item = table.get_item(
        Key={'PK': f'ALBUM#{album_id}', "SK": "METADATA"},
    ).get("Item")

    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': "Album not found"}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        }

    track_records = table.query(
        KeyConditionExpression=Key('PK').eq(f'ALBUM#{album_id}') & Key("SK").begins_with("SONG#")
    ).get("Items") or {}

    track_ids: list[str] = []
    for track_record in track_records:
        track_ids.append(track_record.get("SK").split("#")[-1])

    response = AlbumResponse(
        id=album_id,
        tracks=track_ids
    )
    return {
        'statusCode': 200,
        'body': json.dumps(asdict(response)),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
    }
