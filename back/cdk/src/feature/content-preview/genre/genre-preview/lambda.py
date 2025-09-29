import json
import os
from dataclasses import asdict

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
genre_bucket = os.environ['GENRE_BUCKET']
EXPIRATION_TIME = int(os.environ['EXPIRATION_TIME'])


def lambda_handler(event, _context):
    path_params = event.get('pathParameters') or {}

    genre_id = path_params.get('id')
    if not genre_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Genre id must be present'}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }
    metadata_item = table.get_item(Key={
        'PK': f'GENRE#{genre_id}',
        'SK': f'METADATA'
    }).get("Item")
    if not metadata_item:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Genre not found'}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }

    song_dicts = metadata_item.get("Songs", {})
    song_responses = _get_song_responses(list(song_dicts.values()))
    album_dicts = metadata_item.get("Albums", {})
    album_responses = _get_album_responses(list(album_dicts.values()))
    artist_dicts = metadata_item.get("Artists", {})
    artist_responses = _get_artist_responses(list(artist_dicts.values()))

    response = GenrePreviewResponse(
        id=genre_id,
        artists=artist_responses,
        albums=album_responses,
        songs=song_responses,
        name=metadata_item.get("Name") or '',
        description=metadata_item.get("Description") or '',
        imageUrl=_get_genre_image(metadata_item.get("CoverPath"))
    )
    return {
        'statusCode': 200,
        'body': json.dumps(asdict(response)),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    }


def _get_album_responses(album_records) -> list[GenreAlbumPreviewResponse]:
    album_responses: list[GenreAlbumPreviewResponse] = []
    for album_record in album_records:
        album_responses.append(
            GenreAlbumPreviewResponse(
                imageUrl=_get_album_image(album_record.get("CoverPath")),
                year=album_record.get("ReleaseDate").split("-")[-1],
                id=album_record.get("Id"),
                title=album_record.get("Title"),
                performerNames=[]
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


def _get_song_responses(song_records) -> list[GenreSongPreviewResponse]:
    responses: list[GenreSongPreviewResponse] = []
    for song_record in song_records:
        resp = GenreSongPreviewResponse(
            id=song_record.get('Id'),
            name=song_record.get('Name'),
            imageUrl=_get_song_image(song_record.get("CoverPath")),
        )
        responses.append(resp)

    return responses
def _get_genre_image(cover_path: str):
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": genre_bucket, "Key": cover_path},
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


def _get_artist_responses(artist_records):
    artists: list[GenreArtistPreviewResponse] = []
    for artist_record in artist_records:
        image_url = _get_artist_image(artist_record.get("ImagePath"))
        artists.append(
            GenreArtistPreviewResponse(
                id=artist_record.get("Id"),
                name=artist_record.get("Name"),
                imageUrl=image_url,
            )
        )
    return artists


def _get_artist_image(image_path: str) -> str:
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": artist_bucket, "Key": image_path},
            ExpiresIn=EXPIRATION_TIME,
        )
    except Exception:
        return None
