import os
import json
import boto3
from boto3.dynamodb.conditions import Key
from dataclasses import asdict

from model.songs_response import Song, SongsResponse

EXPIRATION_TIME = int(os.environ.get("EXPIRATION_TIME"))
BUCKET_NAME = os.environ['BUCKET']
TABLE_NAME = os.environ['DYNAMO']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)
s3_client = boto3.client("s3")


def lambda_handler(event, context):
    try:
        limit = int(event.get("queryStringParameters", {}).get("limit", 10))
        last_key = event.get("queryStringParameters", {}).get("lastToken")

        query_params = {
            "IndexName": "SongsIndex",
            "KeyConditionExpression": Key("EntityType").eq("SONG") & Key("SK").eq("METADATA"),
            "Limit": limit
        }

        if last_key:
            query_params["ExclusiveStartKey"] = json.loads(last_key)

        db_response = table.query(**query_params)

        items = db_response.get("Items", [])
        last_evaluated_key = db_response.get("LastEvaluatedKey")

        songs = [
            Song(
                id=item['PK'].split('#')[1],
                name=item.get("Name", ""),
                imageUrl=_get_cover_url(item['PK'].split('#')[1]),
                songUrl=_get_audio_url(item['PK'].split('#')[1])
            )
            for item in items
        ]

        response = SongsResponse(
            songs=songs,
            lastToken=json.dumps(last_evaluated_key) if last_evaluated_key else None
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


def _get_cover_url(song_id: str):
    prefix = f"{song_id}/image/"
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

def _get_audio_url(song_id: str):
    prefix = f"{song_id}/audio/"
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

