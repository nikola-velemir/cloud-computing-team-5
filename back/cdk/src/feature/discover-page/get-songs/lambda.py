import os
import json
import boto3
from dataclasses import asdict

from model.songs_response import Song, SongsResponse

TABLE_NAME = os.environ['DYNAMO']
EXPIRATION_TIME = int(os.environ.get("EXPIRATION_TIME"))
BUCKET_NAME = os.environ['BUCKET']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)
s3_client = boto3.client("s3")


def lambda_handler(event, context):
    try:
        artist_id = event.get('queryStringParameters', {}).get('artistId')
        album_id = event.get('queryStringParameters', {}).get('albumId')
        genre_id = event.get('queryStringParameters', {}).get('genreId')
        if artist_id:
            db_response = table.get_item(
                Key={
                    "PK": f"ARTIST#{artist_id}",
                    "SK": "METADATA"
                }
            )
        else:
            db_response = table.get_item(
                Key={
                    "PK": f"ALBUM#{album_id}",
                    "SK": "METADATA"
                }
            )


        items = db_response.get("Item", {}).get("Songs",{})

        songs = []
        for song_id, song_data in items.items():
            if song_data.get("GenreId").eq(genre_id):
                song = Song(
                    Id=song_id,
                    Name=song_data.get("Name", ""),
                    CoverImage=_get_cover_url(song_data.get("CoverPath"))
                )
                songs.append(song)

        response = SongsResponse(
            songs=songs,
        )
        return {
            "statusCode": 200,
            "body": json.dumps(asdict(response)),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }

def _get_cover_url(cover_path: str):
    if not cover_path: return  None;

    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": cover_path},
        ExpiresIn=EXPIRATION_TIME,
    )