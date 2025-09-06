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

    song_responses = _get_song_responses(artist_id)
    album_responses = _get_album_responses(artist_id)

    response = ArtistViewResponse(
        id=artist_id,
        songs=song_responses,
        name=metadata_item.get('Name') or (metadata_item.get("FirstName") + " " + metadata_item.get("LastName")),
        albums=album_responses,
        biography=metadata_item.get('Biography'),
        imageUrl=_get_artist_image(artist_id, metadata_item.get('ImageType')),
    )
    return {
        'statusCode': 200,
        'body': json.dumps(asdict(response)),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    }


def _get_album_responses(artist_id: str):
    condition = Key("PK").eq(f'ARTIST#{artist_id}') & Key("SK").begins_with("ALBUM#")
    album_item = table.query(
        KeyConditionExpression=condition
    ).get('Items', [])
    album_responses: list[ArtistViewAlbumResponse] = []
    for album in album_item:
        album_id = album['SK'].split("#")[-1];
        album_responses.append(
            ArtistViewAlbumResponse(
                id=album_id,
                imageUrl=_get_album_image(album_id, album.get("ImageType")),
                title=album.get("Title"),
                year=album.get("ReleaseDate", '00-00-0000').split('-')[-1],
            )
        )
    return album_responses


def _get_album_image(album_id: str, image_type: str):
    key = f'{album_id}/cover/cover.{image_type}'
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": album_bucket, "Key": key},
        ExpiresIn=EXPIRATION_TIME,
    )


def _get_song_responses(artist_id) -> list[ArtistViewSongResponse]:
    key = Key('PK').eq(f"ARTIST#{artist_id}") & Key("SK").begins_with("SONG#")
    db_response = table.query(
        KeyConditionExpression=key
    )
    items = db_response.get('Items', [])

    responses: list[ArtistViewSongResponse] = []
    for item in items:
        resp = ArtistViewSongResponse(
            id=item.get('SK').split('#')[-1],
            name=item.get('Name'),
            imageUrl=_get_song_image(item.get("SK").split("#")[-1], item.get("ImageType")),
        )
        responses.append(resp)

    return responses

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
