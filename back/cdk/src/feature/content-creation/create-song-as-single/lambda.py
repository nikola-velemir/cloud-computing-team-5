import json
import os
import uuid
import boto3

TABLE_NAME = os.environ['DYNAMO']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


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
    artist_ids =  body.get("artistIds", [])
    item = {
        'PK': f"SONG#{song_id}",
        "SK": "METADATA",
        "Name": body.get("name"),
        "GenreId": body.get("genreId"),
        "ArtistIds": artist_ids,
        "ReleaseDate": body.get("releaseDate"),
        "ImageType": body.get("imageType"),
        "AlbumId": None,
    }

    table.put_item(Item=item)
    for artist_id in artist_ids:
        artist_song_record = {
            "PK": f"ARTIST#{artist_id}",
            "SK": f"SONG#{song_id}",
            "Name": body.get("name"),
            "GenreId": body.get("genreId"),
            "AudioType": body.get("audioType"),
            "ImageType": body.get("imageType"),
        }
        table.put_item(Item=artist_song_record)

    return {
        "statusCode": 201,
        "body": json.dumps({
            "songId": song_id,
            "songName": body.get("songName"),
            "genreId": body.get("genreId")
        }),
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    }
