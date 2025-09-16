import json
import os
from dataclasses import asdict
from error_handling import with_error_handling
from model.models import ArtistSongPreviewResponse, AlbumSongPreviewResponse, SongPreviewResponse
import boto3

TABLE_NAME = os.environ['DYNAMO']

REGION = os.environ['REGION']
s3_client = boto3.client('s3', region_name=REGION)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)
song_bucket = os.environ['SONG_BUCKET']
artist_bucket = os.environ['ARTIST_BUCKET']
album_bucket = os.environ['ALBUM_BUCKET']
EXPIRATION_TIME = int(os.environ['EXPIRATION_TIME'])


@with_error_handling(["Admin", "AuthenticatedUser"])
def lambda_handler(event, context):
    path_params = event.get('pathParameters') or {}

    song_id = path_params.get('id')
    if not song_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'song id must be present'}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }

    metadata_item = table.get_item(Key={
        'PK': f'SONG#{song_id}',
        'SK': f'METADATA'
    }).get("Item")
    if not metadata_item:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Song not found'}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }

    artist_dicts = metadata_item.get("Artists") or {}
    artist_responses = _get_artist_responses(list(artist_dicts.values()))

    album_dict = metadata_item.get("Album") or {}
    album_response = _get_album_response(album_dict)

    song_response: SongPreviewResponse = SongPreviewResponse(
        id=song_id,
        imageUrl=_get_song_image(metadata_item.get("CoverPath")),
        name=metadata_item.get('Name'),
        artists=artist_responses,
        album=album_response,
        lyrics=_get_song_lyrics(metadata_item.get("LyricsPath")),
    )

    return {
        'statusCode': 200,
        'body': json.dumps(
            asdict(song_response)
        ),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    }


def _get_album_response(album_record):
    return AlbumSongPreviewResponse(
        imageUrl=_get_album_image(album_record.get("CoverPath")),
        title=album_record.get("Title"),
        year=album_record.get("ReleaseDate", '00-00-0000').split('-')[-1],
        id=album_record.get("Id")
    )


def _get_artist_responses(artist_records):
    artists: list[ArtistSongPreviewResponse] = []
    for artist_record in artist_records:
        print(artist_record)

        image_url = _get_artist_image(artist_record.get("ImagePath"))
        artists.append(
            ArtistSongPreviewResponse(
                id=artist_record.get("Id"),
                name=artist_record.get("Name") or f'{artist_record.get("FirstName")} {artist_record.get("LastName")}',
                imageUrl=image_url,
            )
        )
    return artists


def _get_album_image(cover_path):
    if not cover_path: return None;
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": album_bucket, "Key": cover_path},
            ExpiresIn=EXPIRATION_TIME,
        )
    except Exception:
        return None


def _get_artist_image(cover_path: str):
    if not cover_path: return None;
    try:

        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": artist_bucket, "Key": cover_path},
            ExpiresIn=EXPIRATION_TIME,
        )
    except Exception:
        return None

def _get_song_lyrics(lyrics_path:str):
    if not lyrics_path: return None;
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket":song_bucket, "Key": lyrics_path},
            ExpiresIn=EXPIRATION_TIME,
        )
    except Exception:
        return None

def _get_song_image(cover_path: str):
    if not cover_path: return None;
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": song_bucket, "Key": cover_path},
            ExpiresIn=EXPIRATION_TIME,
        )
    except Exception:
        return None
