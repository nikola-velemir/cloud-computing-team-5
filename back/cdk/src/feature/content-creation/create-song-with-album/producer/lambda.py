import datetime
import json
import os
import uuid
from dataclasses import asdict

import boto3

TABLE_NAME = os.environ['DYNAMO']
QUEUE_URL = os.environ['QUEUE_URL']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

sqs = boto3.client('sqs')

from model.song_metada_record import *
from error_handling import with_error_handling


@with_error_handling(["Admin"])
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
    lyrics_path = f'{song_id}/lyrics/lyrics'
    duration = body.get("duration") or 0
    artists = _get_artist_records(artist_ids)
    album = _get_album_record(album_id)
    genre = _get_genre_record(genre_id)
    release_date = body.get("releaseDate") or datetime.datetime.utcnow().strftime("%d-%m-%Y")
    created_at = datetime.datetime.utcnow().strftime("%d-%m-%Y")
    metadata_record: SongMetadataRecord = SongMetadataRecord(
        PK=f"SONG#{song_id}",
        Name=body.get("name") or "",
        CoverPath=cover_path,
        AudioPath=audio_path,
        Artists=artists,
        Album=album,
        LyricsPath=lyrics_path,
        ReleaseDate=release_date,
        CreatedAt=created_at,
        Genre=genre,
        Duration=duration,
        UpdatedAt=datetime.datetime.utcnow().isoformat()
    )
    print(metadata_record.EntityType)
    table.put_item(Item=asdict(metadata_record))
    other_record = AlbumSongRecord(
        Id=song_id,
        Name=body.get("name") or "",
        CoverPath=cover_path,
        AudioPath=audio_path,
        CreatedAt=created_at,
        ReleaseDate=release_date,
        Duration=duration,
        GenreId=genre_id
    )
    _write_into_genre(genre_id, asdict(other_record))
    _write_into_album(album_id, asdict(other_record))
    _write_into_artists(artist_ids, asdict(other_record))
    message = {
        "type": "SONG_CREATED",
        "song_id": song_id,
        "name": body.get("name") or "",
        "cover_path": cover_path,
        "audio_path": audio_path,
        "release_date": release_date,
        "duration": duration,
        "genre_id": genre_id,
        "artist_ids": artist_ids,
    }
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message),
        MessageGroupId=f"{metadata_record.PK}"  # or artist
    )
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
    song_id = song["Id"]
    table.update_item(
        Key={"PK": f"ALBUM#{album_id}", "SK": "METADATA"},
        UpdateExpression="SET Songs.#song_id = :song",
        ExpressionAttributeNames={"#song_id": song_id},
        ExpressionAttributeValues={":song": song},
        ReturnValues="UPDATED_NEW"
    )


def _write_into_genre(genre_id, song):
    song_id = song["Id"]
    table.update_item(
        Key={"PK": f"GENRE#{genre_id}", "SK": "METADATA"},
        UpdateExpression="SET Songs.#song_id = :song",
        ExpressionAttributeNames={"#song_id": song_id},
        ExpressionAttributeValues={":song": song},
        ReturnValues="UPDATED_NEW"
    )


def _write_into_artists(artist_ids, song):
    song_id = song["Id"]
    for artist_id in artist_ids:
        table.update_item(
            Key={"PK": f"ARTIST#{artist_id}", "SK": "METADATA"},
            UpdateExpression="SET Songs.#song_id = :song",
            ExpressionAttributeNames={"#song_id": song_id},
            ExpressionAttributeValues={":song": song},
            ReturnValues="UPDATED_NEW"
        )


def _get_artist_records(artist_ids) -> dict[str, ArtistRecord]:
    artist_records: dict[str, ArtistRecord] = {}
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

        artist_records[artist_id] = artist_record

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
