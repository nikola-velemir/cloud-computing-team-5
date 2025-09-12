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

    album_id = path_params.get('id')
    if not album_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Album id must be present'}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }

    metadata_item = table.get_item(Key={
        'PK': f'ALBUM#{album_id}',
        'SK': f'METADATA'
    }).get("Item")

    artist_dicts = metadata_item.get('Artists', {})
    artist_responses = _get_artist_responses(list(artist_dicts.values()))
    song_dicts = metadata_item.get("Songs",[])
    song_responses = _get_song_responses(list(song_dicts.values()))

    album_response: AlbumPreviewResponse = AlbumPreviewResponse(
        id=album_id,
        imageUrl=_get_album_image(metadata_item.get("CoverPath") or "AAA"),
        artists=artist_responses,
        songs=song_responses,
        releaseDate=metadata_item.get("ReleaseDate", '00-00-0000'),
        title=metadata_item.get("Title", ''),
    )

    return {
        'statusCode': 200,
        'body': json.dumps(
            asdict(album_response)
        ),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    }


def _get_artist_responses(artist_records:list[any]):
    artists: list[ArtistAlbumPreviewResponse] = []
    for artist_record in artist_records:
        artist_name = artist_record.get('Name')
        artist_first_name = artist_record.get('FirstName','')
        artist_last_name = artist_record.get('LastName','')
        artists.append(
            ArtistAlbumPreviewResponse(
                id=artist_record.get("Id"),
                name=artist_name or f'{artist_first_name} {artist_last_name}',
                imageUrl=_get_artist_image(artist_record.get("ImagePath") or ""),
            )
        )
    return artists


def _get_album_image(cover_path):
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": album_bucket, "Key": cover_path},
        ExpiresIn=EXPIRATION_TIME,
    )


def _get_artist_image(cover_path):

    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": artist_bucket, "Key": cover_path},
        ExpiresIn=EXPIRATION_TIME,
    )


def _get_song_image(cover_path):
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": song_bucket, "Key": cover_path},
        ExpiresIn=EXPIRATION_TIME,
    )


def _get_song_responses(song_records:list[any]):

    responses: list[SongAlbumPreviewResponse] = []
    for song_record in song_records:

        resp = SongAlbumPreviewResponse(
            id=song_record.get('Id') or "",
            name=song_record.get('Name'),
            imageUrl=_get_song_image(song_record.get("CoverPath")),
        )
        responses.append(resp)

    return responses
