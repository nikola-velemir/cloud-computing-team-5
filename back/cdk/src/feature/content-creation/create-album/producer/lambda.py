import json
import os
import uuid
from dataclasses import asdict
from datetime import datetime

from model.album_record import *

import boto3

TABLE_NAME = os.environ['DYNAMO']
dynamo = boto3.resource('dynamodb')
table = dynamo.Table(TABLE_NAME)


def lambda_handler(event, context):
    event_body = json.loads(event['body'])
    album_id = str(uuid.uuid4())
    artist_ids = event_body['artistIds']
    genre_ids = event_body['genreIds']
    cover_file_type = event_body['imageType'].split('/')[-1]
    artists: dict[str,ArtistRecord] = _get_artist_records(artist_ids)
    genres = _get_genre_records(genre_ids)
    album = AlbumRecord(
        PK='ALBUM#' + album_id,
        Title=event_body['title'],
        ReleaseDate=event_body['releaseDate'],
        CoverPath=f'{album_id}/cover/cover.{cover_file_type}',
        Artists=artists,
        Songs={},
        Genres=genres,
        UpdatedAt=datetime.utcnow().isoformat()

    )
    table.put_item(Item=asdict(album))
    # album_genre_record = GenreAlbumRecord(
    #     CoverPath=f'{album_id}/cover/cover.{cover_file_type}',
    #     Id=album_id,
    #     ReleaseDate=event_body['releaseDate'],
    #     Title=event_body['title'],
    # )
    # _write_into_genres(genre_ids, asdict(album_genre_record))
    # _write_into_artists(artist_ids, asdict(album_genre_record))
    return {
        'statusCode': 201,
        'body': json.dumps({'albumId': album_id}),
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
    }

def _write_into_artists(artist_ids: list[str], album):
    album_id = album["Id"]

    for artist_id in artist_ids:
        table.update_item(
            Key={"PK": f"ARTIST#{artist_id}", "SK": "METADATA"},
            UpdateExpression="SET Albums.#album_id = :album",
            ExpressionAttributeNames={"#album_id": album_id},
            ExpressionAttributeValues={":album": album},
            ReturnValues="UPDATED_NEW"
        )

def _write_into_genres(genre_ids, album):
    album_id = album["Id"]
    for genre_id in genre_ids:
        table.update_item(
            Key={"PK": f"GENRE#{genre_id}", "SK": "METADATA"},
            UpdateExpression="SET Albums.#album_id = :album",
            ExpressionAttributeNames={"#album_id": album_id},
            ExpressionAttributeValues={":album": album},
            ReturnValues="UPDATED_NEW"
        )


def _get_genre_records(genre_ids: list) -> dict[str,GenreRecord]:
    genres: dict[str,GenreRecord] = {}
    for genre_id in genre_ids:
        genre_table_item = table.get_item(Key={'PK': f'GENRE#{genre_id}', 'SK': "METADATA"}).get("Item")
        if not genre_table_item:
            continue
        genre_name = genre_table_item.get("Name")
        genre_cover_path = genre_table_item.get("CoverPath")
        genre_record = GenreRecord(
            Name=genre_name,
            CoverPath=genre_cover_path,
            Id=genre_id,
        )
        genres[genre_id]=genre_record
    return genres


def _get_artist_records(artist_ids) -> dict[str,ArtistRecord]:
    artist_records: dict[str,ArtistRecord]= {}
    for artist_id in artist_ids:
        artist_table_item = table.get_item(
            Key={'PK': f'ARTIST#{artist_id}', "SK": "METADATA"},
        ).get("Item")
        if not artist_table_item:
            continue
        artist_first_name = artist_table_item.get("FirstName") or ""
        artist_last_name = artist_table_item.get("LastName") or ""
        artist_name = artist_table_item.get("Name") or f'{artist_first_name} {artist_last_name}'
        artist_cover_path = artist_table_item.get("ImagePath")
        artist_record = ArtistRecord(
            Id=artist_id,
            Name=artist_name,
            ImagePath=artist_cover_path,
            FirstName=artist_first_name,
            LastName=artist_last_name,
        )
        artist_records[artist_id] = artist_record

    return artist_records
