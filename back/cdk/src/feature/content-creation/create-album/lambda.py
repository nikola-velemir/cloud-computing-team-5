import json
import os
import uuid
from dataclasses import asdict
from model.artist_album_record import ArtistAlbumRecord
from model.album_record import AlbumRecord

import boto3

TABLE_NAME = os.environ['DYNAMO']
dynamo = boto3.resource('dynamodb')
table = dynamo.Table(TABLE_NAME)


def lambda_handler(event, context):
    event_body = json.loads(event['body'])
    album_id = str(uuid.uuid4())
    artist_ids = event_body['artistIds']
    album = AlbumRecord(
        PK='ALBUM#' + album_id,
        GenreIds=event_body['genreIds'],
        Title=event_body['title'],
        ReleasedDate=event_body['releaseDate'],
        ArtistIds=artist_ids,
        ImageType=event_body['imageType'].split('/')[-1],
    )
    table.put_item(Item=asdict(album))
    for artist_id in artist_ids:
        artist_record = ArtistAlbumRecord(
            PK=f'ARTIST#{artist_id}',
            SK=f'ALBUM#{album_id}',
        )
        table.put_item(Item=asdict(artist_record))

    return {
        'statusCode': 201,
        'body': json.dumps({'albumId': album_id}),
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
    }
