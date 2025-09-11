import os
import json
import boto3
from boto3.dynamodb.conditions import Key
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
        query_params = {
            "KeyConditionExpression": Key("PK").eq("GENRE#"+genre_id) & Key("SK").eq("ARTISTS")
        }

        db_response = table.query(**query_params)

        items = db_response.get("Items", [])

        artists = [
            Artist(
                id=item['PK'].split('#')[1],
                firstName=item.get("FirstName", ""),
                lastName=item.get("LastName", ""),
            )
            for item in items
        ]

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


def _get_cover_url(artist_id: str):
    prefix = f"{artist_id}/image/"
    try:
        resp = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
        contents = resp.get("Contents")
        if not contents:
            return None

        key = contents[0]["Key"]
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": key},
            ExpiresIn=EXPIRATION_TIME
        )
    except Exception as e:
        print("Error:", e)
        return None
