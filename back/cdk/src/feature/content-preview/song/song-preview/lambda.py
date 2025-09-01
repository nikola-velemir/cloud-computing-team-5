import json
import os
from dataclasses import asdict

from model.models import ArtistSongPreviewResponse, AlbumSongPreviewResponse, SongPreviewResponse
import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = os.environ['DYNAMO']

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)
song_bucket = os.environ['SONG_BUCKET']
artist_bucket = os.environ['ARTIST_BUCKET']
album_bucket = os.environ['ALBUM_BUCKET']
EXPIRATION_TIME = int(os.environ['EXPIRATION_TIME'])


def lambda_handler(event, context):
    path_params = event.get('pathParameters') or {}

    song_id = path_params.get('id')
    if not song_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'song id must be present'}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }

    metadata_item =table.get_item(Key={
        'PK': f'SONG#{song_id}',
        'SK': f'METADATA'
    }).get("Item")

    artist_ids = metadata_item.get('ArtistIds', [])
    artist_responses = _get_artist_responses(artist_ids)
    album_response = _get_album_response(album_id=metadata_item.get('AlbumId'))

    song_response: SongPreviewResponse = SongPreviewResponse(
        id=song_id,
        imageUrl=_get_song_image(song_id, metadata_item['ImageType']),
        name=metadata_item.get('Name'),
        artists=artist_responses,
        album=album_response,
    )

    return {
        'statusCode': 200,
        'body': json.dumps(
            asdict(song_response)
        ),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    }


def _get_album_response(album_id: str):
    print(album_id)
    album_item = table.get_item(
        Key={
            "PK": f"ALBUM#{album_id}",
            "SK": "METADATA"
        }
    ).get('Item')
    return AlbumSongPreviewResponse(
        imageUrl=_get_album_image(album_id, album_item.get("ImageType")),
        title=album_item.get("Title"),
        year=album_item.get("ReleasedDate", '00-00-0000').split('-')[-1],
        id=album_id
    )


def _get_artist_responses(artistIds: list[str]):
    artists: list[ArtistSongPreviewResponse] = []
    for artistId in artistIds:
        print(artistId)
        artist_item = table.get_item(
            Key={
                "PK": f"ARTIST#{artistId}",
                "SK": "METADATA"
            }
        ).get("Item")
        print(artist_item)
        image_url = _get_artist_image(artistId, artist_item.get("ImageType"))
        artists.append(
            ArtistSongPreviewResponse(
                id=artistId,
                name=artist_item.get('Name'),
                imageUrl=image_url,
            )
        )
    return artists


def _get_album_image(album_id: str, image_type: str):
    key = f'{album_id}/cover/cover.{image_type}'
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": album_bucket, "Key": key},
        ExpiresIn=EXPIRATION_TIME,
    )


def _get_artist_image(artist_id: str, image_type: str):
    key = f'{artist_id}/image/image.{image_type}'
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": artist_bucket, "Key": key},
        ExpiresIn=EXPIRATION_TIME,
    )


def _get_song_image(song_id, image_type: str):
    key = f'{song_id}/image/image.{image_type}'
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": song_bucket, "Key": key},
        ExpiresIn=EXPIRATION_TIME,
    )
