import json
import os
from dataclasses import asdict

from boto3.dynamodb.conditions import Key

from model.model import *
import boto3

TABLE_NAME = os.environ['DYNAMO']

REGION = os.environ['REGION']
s3_client = boto3.client('s3',region_name = REGION)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)
song_bucket = os.environ['SONG_BUCKET']
artist_bucket = os.environ['ARTIST_BUCKET']
album_bucket = os.environ['ALBUM_BUCKET']
EXPIRATION_TIME = int(os.environ['EXPIRATION_TIME'])


def lambda_handler(event, context):
    path_params = event.get('pathParameters') or {}

    artist_id = path_params.get('id')
    if not artist_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Album id must be present'}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }

    metadata_item = table.get_item(Key={
        'PK': f'ARTIST#{artist_id}',
        'SK': f'METADATA'
    }).get("Item")

    song_dicts = metadata_item.get("Songs") or {}
    song_responses = _get_song_responses(list(song_dicts.values()))
    album_dicts = metadata_item.get("Albums") or {}
    album_responses = _get_album_responses(list(album_dicts.values()))

    response = ArtistViewResponse(
        id=artist_id,
        songs=song_responses,
        name=metadata_item.get('Name') or (metadata_item.get("FirstName") + " " + metadata_item.get("LastName")),
        albums=album_responses,
        biography=metadata_item.get('Biography') or '',
        imageUrl=_get_artist_image(metadata_item.get('ImagePath')),
    )
    return {
        'statusCode': 200,
        'body': json.dumps(asdict(response)),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    }


def _get_album_responses(album_records):
    album_responses: list[ArtistViewAlbumResponse] = []
    for album_record in album_records:
        album_responses.append(
            ArtistViewAlbumResponse(
                id=album_record.get("Id"),
                imageUrl=_get_album_image(album_record.get("CoverPath")),
                title=album_record.get("Title"),
                year=album_record.get("ReleaseDate", '00-00-0000').split('-')[-1],
            )
        )
    return album_responses


def _get_album_image(cover_path):
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": album_bucket, "Key": cover_path},
            ExpiresIn=EXPIRATION_TIME,
        )
    except Exception:
        return None


def _get_song_responses(song_records: list[any]) -> list[ArtistViewSongResponse]:
    responses: list[ArtistViewSongResponse] = []
    for song_record in song_records:
        resp = ArtistViewSongResponse(
            id=song_record.get('Id'),
            name=song_record.get('Name'),
            imageUrl=_get_song_image(song_record.get("CoverPath")),
        )
        responses.append(resp)

    return responses


def _get_artist_image(image_path: str) -> str:
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": artist_bucket, "Key": image_path},
            ExpiresIn=EXPIRATION_TIME,
        )
    except Exception:
        return None


def _get_song_image(cover_path: str):
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": song_bucket, "Key": cover_path},
            ExpiresIn=EXPIRATION_TIME,
        )
    except Exception:
        return None
