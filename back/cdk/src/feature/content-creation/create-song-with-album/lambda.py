import json
import os
import uuid
from dataclasses import asdict

import boto3

TABLE_NAME = os.environ['DYNAMO']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)
from model.song_metada_record import SongMetadataRecord
from model.album_song_record import AlbumSongRecord

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
    except Exception:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid JSON"}),
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
        }

    song_id = str(uuid.uuid4())
    album_id = body.get("albumId")
    metadata_record: SongMetadataRecord = SongMetadataRecord(
        PK=f"SONG#{song_id}",
        ArtistIds=body.get("artistIds", []),
        Name=body.get("name"),
        GenreId=body.get("genreId"),
        AlbumId=album_id,
        AudioType= body['audioType'].split("/")[-1],
        ImageType=body['imageType'].split('/')[-1],
        ReleaseDate=body.get("releaseDate"),
    )
    table.put_item(Item=asdict(metadata_record))

    album_record: AlbumSongRecord = AlbumSongRecord(
        PK=f"ALBUM#{album_id}",
        SK=f"SONG#{song_id}",
        Name=body.get("name"),
    )
    table.put_item(Item=asdict(album_record))

    return {
        "statusCode": 201,
        "body": json.dumps({
            "songId": song_id,
            "songName": body.get("songName"),
            "genreId": body.get("genreId")
        }),
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    }
