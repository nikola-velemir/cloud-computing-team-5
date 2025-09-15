import os
import json
import boto3
from dataclasses import asdict

from model.artists_response import Artist, ArtistsResponse

EXPIRATION_TIME = int(os.environ.get("EXPIRATION_TIME"))
BUCKET_NAME = os.environ['BUCKET']
TABLE_NAME = os.environ['DYNAMO']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)
s3_client = boto3.client("s3")


def lambda_handler(event, context):
    try:
        genre_id = event.get('queryStringParameters', {}).get('genreId')

        db_response = table.get_item(
            Key={
                "PK": f"GENRE#{genre_id}",
                "SK": "METADATA"
            }
        )

        items = db_response.get("Item", {}).get("Artists", {})

        artists = []
        for artist_id, artist_data in items.items():
            artist = Artist(
                id = artist_id,
                name=artist_data.get("name"),
            )
            artists.append(artist)

        response = ArtistsResponse(
            artists=artists,
        )
        return {
            "statusCode": 200,
            "body": json.dumps(asdict(response)),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"exception": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }