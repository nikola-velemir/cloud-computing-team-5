import json
import os
from dataclasses import asdict

import jwt
from error_handling import with_error_handling
from model.model import TrackResponse

import boto3

TABLE_NAME = os.environ["TABLE_NAME"]
SONGS_BUCKET = os.environ["SONGS_BUCKET"]
EXPIRATION_TIME = int(os.environ["EXPIRATION_TIME"])
REGION = os.environ['REGION']
s3_client = boto3.client('s3',region_name = REGION)
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)
FEED_QUEUE_URL = os.environ["FEED_QUEUE_URL"]
sqs = boto3.client("sqs")


@with_error_handling(["Admin","AuthenticatedUser"])
def lambda_handler(event, _context):
    headers = event.get("headers", {})
    auth_header = headers.get("Authorization")
    if not auth_header:
        return {"statusCode": 401, "body": "Missing Authorization header"}

    token = auth_header.split(" ")[1]

    claims = jwt.decode(token, options={"verify_signature": False})
    print("JWT Claims:", claims)

    user_id = claims.get("sub")
    track_id = event['pathParameters'].get('id')

    track_item = table.get_item(
        Key={
            "PK": f'SONG#{track_id}',
            "SK": 'METADATA'
        }
    ).get("Item")
    if not track_item:
        return {
            'statusCode': 404,
            'body': json.dumps({
                'message': 'Song not found'
            }),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }
    artist_ids = track_item.get("ArtistIds")
    response: TrackResponse = TrackResponse(
        id=track_id,
        name=track_item.get("Name"),
        duration=int(track_item.get("Duration")) or 0,
        artistNames=_get_artist_names(artist_ids),
        audioUrl=_get_song_audio(track_item.get("AudioPath")),
    )
    feed_event = {
        "type": "PLAY_SONG",
        "body": {
            "entityType": "SONG",
            "entityId": track_id,
            "name": track_item.get("Name"),
            "userId": user_id
        }
    }
    _send_to_feed(feed_event)

    return {
        'statusCode': 200,
        'body': json.dumps(asdict(response)),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}

    }

def _send_to_feed(payload: dict):
    sqs.send_message(
        QueueUrl=FEED_QUEUE_URL,
        MessageBody=json.dumps(payload)
    )

def _get_song_image(cover_path):
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": SONGS_BUCKET, "Key": cover_path},
        ExpiresIn=EXPIRATION_TIME,
    )

def _get_song_audio(audio_path):
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": SONGS_BUCKET, "Key": audio_path},
            ExpiresIn=EXPIRATION_TIME,
        )
    except Exception:
        return None


def _get_artist_names(artist_ids: list[str]):
    return []
    artist_names: list[str] = []
    for artist_id in artist_ids:
        item = table.get_item(
            Key={
                "PK": f'ARTIST#{artist_id}',
                "SK": 'METADATA'
            }
        ).get("Item")
        if not item: continue;
        artist_names.append(item.get("Name"))
    return artist_names
