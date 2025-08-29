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

    item = {
        'PK': f"SONG#{song_id}",
        "SK": "METADATA",
        "Name": body.get("songName"),
        "GenreId": body.get("genreId"),
        "ArtistIds": body.get("artistIds", []),
        "ReleaseDate": body.get("releaseDate"),
        "AlbumId": None,
    }

    table.put_item(Item=item)

    return {
        "statusCode": 201,
        "body": json.dumps({
            "songId": song_id,
            "songName": body.get("songName"),
            "genreId": body.get("genreId")
        }),
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    }
