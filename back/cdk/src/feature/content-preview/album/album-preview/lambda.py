import json
import os
from dataclasses import asdict

from boto3.dynamodb.conditions import Key

from model.model import *
import boto3

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

    artist_ids = metadata_item.get('ArtistIds', [])
    artist_responses = _get_artist_responses(artist_ids)
    song_responses = _get_song_responses(album_id=album_id)

    album_response: AlbumPreviewResponse = AlbumPreviewResponse(
        id=album_id,
        imageUrl=_get_album_image(album_id, metadata_item.get("ImageType")),
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


def _get_artist_responses(artistIds: list[str]):
    artists: list[ArtistAlbumPreviewResponse] = []
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
            ArtistAlbumPreviewResponse(
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


def _get_song_responses(album_id):
    key = Key('PK').eq(f"ALBUM#{album_id}") & Key("SK").begins_with("SONG#")
    db_response = table.query(
        KeyConditionExpression=key
    )
    items = db_response.get('Items', [])
    responses: list[SongAlbumPreviewResponse] = [
        SongAlbumPreviewResponse(
            id=item.get('PK').split('#')[-1],
            name=item.get('Name'),
            imageUrl=_get_song_image(item.get("PK").split("#")[-1], item.get("ImageType")),
        )
        for item in items
    ]
    return responses
