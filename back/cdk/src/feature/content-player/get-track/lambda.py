import json
import os
from dataclasses import asdict

from model.model import TrackResponse

import boto3

TABLE_NAME = os.environ["TABLE_NAME"]
SONGS_BUCKET = os.environ["SONGS_BUCKET"]
EXPIRATION_TIME = int(os.environ["EXPIRATION_TIME"])
s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, _context):
    track_id = event['pathParameters'].get('id')
    if not track_id:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Song id is mendatory'
            }),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }

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
    return {
        'statusCode': 200,
        'body': json.dumps(asdict(response)),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}

    }

def _get_song_image(cover_path):
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": SONGS_BUCKET, "Key": cover_path},
        ExpiresIn=EXPIRATION_TIME,
    )

def _get_song_audio(audio_path):
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": SONGS_BUCKET, "Key": audio_path},
        ExpiresIn=EXPIRATION_TIME,
    )


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
