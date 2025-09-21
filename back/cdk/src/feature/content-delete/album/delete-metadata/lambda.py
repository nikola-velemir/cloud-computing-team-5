import os
import json
import boto3
from boto3.dynamodb.conditions import Key
from error_handling import with_error_handling

lambda_client = boto3.client('lambda')
dynamodb = boto3.resource('dynamodb')

s3_client = boto3.client("s3")
BUCKET_NAME = os.environ["S3_BUCKET"]

TABLE_NAME = os.environ['DYNAMO']
dynamo = boto3.resource('dynamodb')
table = dynamo.Table(TABLE_NAME)

@with_error_handling(["Admin"])
def lambda_handler(event, context):
    print(event)
    album_id = event['pathParameters']['id']
    pk = f"ALBUM#{album_id}"
    sk = "METADATA"

    response = table.get_item(Key={"PK": pk, "SK": sk})
    item = response.get("Item")
    print(item)
    if item is not None:
        genre_ids = [genre["Id"] for genre in item["Genres"].values()]
        song_ids = [song["Id"] for song in item["Songs"].values()]
        artist_ids = [artist["Id"] for artist in item["Artists"].values()]

        invoke_delete_review_lambda(album_id)
        invoke_delete_subscriptions_lambda(album_id)
        claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
        invoke_delete_songs_lambda(song_ids, album_id,claims)
        invoke_delete_artists_lambda(album_id, artist_ids)
        invoke_delete_genre_lambda(album_id, genre_ids)
        delete_album_folders(album_id)
        table.delete_item(Key={"PK": pk, "SK": sk})
        invoke_delete_feed_lambda(album_id)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PUT,DELETE",
                "Access-Control-Allow-Headers": "Content-Type,Authorization"
            },
            "body": json.dumps(True)
        }
    return None

def delete_album_folders(album_id):
    prefix = f"{album_id}/"

    response = s3_client.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=prefix
    )

    if "Contents" in response:
        objects_to_delete = [{"Key": obj["Key"]} for obj in response["Contents"]]

        s3_client.delete_objects(
            Bucket=BUCKET_NAME,
            Delete={"Objects": objects_to_delete}
        )

def invoke_delete_artists_lambda(album_id, artist_ids):
    payload = {
        "album_id": album_id,
        "artist_ids": artist_ids
    }
    lambda_client.invoke(
        FunctionName=os.environ['DELETE_FROM_ARTISTS_LAMBDA_NAME'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def invoke_delete_feed_lambda(album_id):
    payload = {
        "album_id": album_id,
    }
    lambda_client.invoke(
        FunctionName=os.environ['DELETE_FROM_FEED_LAMBDA_NAME'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def invoke_delete_genre_lambda(album_id, genre_ids):
    payload = {
        "album_id": album_id,
        "genre_ids": genre_ids
    }
    lambda_client.invoke(
        FunctionName=os.environ['DELETE_FROM_GENRE_LAMBDA_NAME'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def invoke_delete_review_lambda(album_id):
    payload = {
        "album_id": album_id,
    }
    lambda_client.invoke(
        FunctionName=os.environ['DELETE_FROM_REVIEWS_LAMBDA_NAME'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )
def invoke_delete_subscriptions_lambda(album_id):
    payload = {
        "album_id": album_id,
    }
    lambda_client.invoke(
        FunctionName=os.environ['DELETE_FROM_SUBSCRIPTIONS_LAMBDA_NAME'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def invoke_delete_songs_lambda(song_ids, album_id, claims):
    payload = {
        "song_ids": song_ids,
        "album_id": album_id,
        "requestContext": {
            "authorizer": {
                "claims": claims
            }
        }
    }
    lambda_client.invoke(
        FunctionName=os.environ['DELETE_SONGS_LAMBDA_NAME'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

