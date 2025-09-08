import datetime
import json
import os
import uuid
from dataclasses import asdict

import boto3

TABLE_NAME = os.environ['DYNAMO']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)
from model.song_metada_record import *


def lambda_handler(event, _context):
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
    genre_id = body.get("genreId")
    artist_ids = body.get("artistIds", [])
    audio_type = body['audioType'].split("/")[-1]
    cover_type = body["imageType"].split("/")[-1]
    audio_path = f'{song_id}/audio/audio.{audio_type}'
    cover_path = f'{song_id}/cover/cover.{cover_type}'
    duration = body.get("duration")
    artists = _get_artist_records(artist_ids)
    album = _get_album_record(album_id)
    genre = _get_genre_record(genre_id)
    release_date = body.get("releaseDate") or datetime.datetime.utcnow().strftime("%d-%m-%Y")
    metadata_record: SongMetadataRecord = SongMetadataRecord(
        PK=f"SONG#{song_id}",
        Name=body.get("name") or "",
        CoverPath=cover_path,
        AudioPath=audio_path,
        Artists=artists,
        Album=album,
        ReleaseDate=release_date,
        CreatedAt=datetime.datetime.utcnow().strftime("%d-%m-%Y"),
        Genre=genre,
        Duration=duration,
    )
    table.put_item(Item=asdict(metadata_record))
    song_album_record = AlbumSongRecord(
        ReleaseDate= release_date,
        CoverPath=cover_path,
        Id=song_id,
        AudioPath=audio_path,
        Name=body.get("name") or "",
        CreatedAt=datetime.datetime.utcnow().strftime("%d-%m-%Y"),
        Duration=duration,
    )
    _write_into_album(album_id, asdict(song_album_record))
    _write_into_genre(genre_id, asdict(song_album_record))
    _write_into_artists(artist_ids, asdict(song_album_record))
    return {
        "statusCode": 201,
        "body": json.dumps({
            "songId": song_id,
            "songName": body.get("songName"),
            "genreId": body.get("genreId")
        }),
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    }


def _write_into_album(album_id, song):

    table.update_item(
        Key={"PK": f"ALBUM#{album_id}", "SK": "METADATA"},
        UpdateExpression="SET #lst = list_append(#lst, :new_items)",
        ExpressionAttributeNames={"#lst": "Songs"},
        ExpressionAttributeValues={":new_items": [song]},
        ReturnValues="UPDATED_NEW"
    )
def _write_into_genre(genre_id, song):
    table.update_item(
        Key={"PK": f"GENRE#{genre_id}", "SK": "METADATA"},
        UpdateExpression="SET #lst = list_append(#lst, :new_items)",
        ExpressionAttributeNames={"#lst": "Songs"},
        ExpressionAttributeValues={":new_items": [song]},
        ReturnValues="UPDATED_NEW"
    )
def _write_into_artists(artist_ids, song):
    for artist_id in artist_ids:
        table.update_item(
            Key={"PK": f"ARTIST#{artist_id}", "SK": "METADATA"},
            UpdateExpression="SET #lst = list_append(#lst, :new_items)",
            ExpressionAttributeNames={"#lst": "Songs"},
            ExpressionAttributeValues={":new_items": [song]},
            ReturnValues="UPDATED_NEW")

def _get_artist_records(artist_ids) -> list[ArtistRecord]:
    artist_records: list[ArtistRecord] = []
    for artist_id in artist_ids:
        artist_table_item = table.get_item(
            Key={"PK": f"ARTIST#{artist_id}", "SK": "METADATA"},
        ).get("Item")

        if not artist_table_item:
            continue
        artist_first_name = artist_table_item.get("FirstName") or ""
        artist_last_name = artist_table_item.get("LastName") or ""
        artist_name = artist_table_item.get("Name") or f'{artist_first_name} {artist_last_name}'
        artist_cover_path = artist_table_item.get("ImagePath")
        artist_record = ArtistRecord(
            Id=artist_table_item.get("PK").split("#")[-1],
            Name=artist_name,
            LastName=artist_last_name,
            FirstName=artist_first_name,
            ImagePath=artist_cover_path
        )

        artist_records.append(artist_record)

    return artist_records


def _get_genre_record(genre_id) -> GenreRecord | None:
    genre_table_item = table.get_item(
        Key={"PK": f"GENRE#{genre_id}", "SK": "METADATA"},
    ).get("Item")
    if not genre_table_item:
        return None
    genre_record = GenreRecord(
        Id=genre_id,
        CoverPath=genre_table_item.get("CoverPath"),
        Name=genre_table_item.get("Name"),
    )
    return genre_record


def _get_album_record(album_id) -> AlbumRecord | None:
    album_table_item = table.get_item(
        Key={"PK": f"ALBUM#{album_id}", "SK": "METADATA"},
    ).get("Item")
    if not album_table_item:
        return None
    album_record = AlbumRecord(
        Id=album_id,
        CoverPath=album_table_item.get("CoverPath"),
        Title=album_table_item.get("Title"),
    )
    return album_record
