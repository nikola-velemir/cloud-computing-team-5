import json
import os
from dataclasses import asdict

import boto3
from error_handling import with_error_handling

from model.model import AlbumResponse

TABLE_NAME = os.environ['TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)
FEED_QUEUE_URL = os.environ["FEED_QUEUE_URL"]
sqs = boto3.client("sqs")


@with_error_handling(["Admin","AuthenticatedUser"])
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

    track_records = item.get("Songs") or {}
    tracks = []
    for track_id, track_data in track_records.items():
        tracks.append({
            "Id": track_id,
            "Name": track_data.get("Name"),
            "CoverImage": track_data.get("CoverPath")
        })
    payload = {
        "type": "PLAY_ALBUM",
        "body": {
            "entityType": "ALBUM",
            "entityId": album_id,
            "metadata": {
                "name": item.get("Name"),
                "coverImage": item.get("CoverPath"),
            },
            "tracks": tracks
        }
    }
    _send_to_feed(payload)
    return {
        'statusCode': 200,
        'body': json.dumps(asdict(response)),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
    }

def _send_to_feed(payload: dict):
    sqs.send_message(
        QueueUrl=FEED_QUEUE_URL,
        MessageBody=json.dumps(payload)
    )
