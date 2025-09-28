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
    song_id = event['pathParameters']['id']
    pk = f"SONG#{song_id}"
    sk = "METADATA"

    response = table.get_item(Key={"PK": pk, "SK": sk})
    item = response.get("Item")
    if item is not None:
        genre = item["Genre"]["Id"]
        album = item["Album"]["Id"]
        artists = [artist["Id"] for artist in item["Artists"].values()]

        invoke_delete_genre_lambda(song_id, genre)
        invoke_delete_review_lambda(song_id)
        invoke_delete_artists_lambda(song_id, artists)
        invoke_delete_album_lambda(song_id, album)
        invoke_delete_feed_lambda(song_id)
        delete_song_folders(song_id)
        table.delete_item(Key={"PK": pk, "SK": sk})

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

def delete_song_folders(song_id):
    prefix = f"{song_id}/"

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

def invoke_delete_genre_lambda(song_id, genre_id):
    payload = {
        "song_id": song_id,
        "genre_id": genre_id
    }
    lambda_client.invoke(
        FunctionName=os.environ['DELETE_FROM_GENRES_LAMBDA_NAME'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def invoke_delete_feed_lambda(song_id):
    payload = {
        "song_id": song_id,
    }
    lambda_client.invoke(
        FunctionName=os.environ['DELETE_FROM_FEED_LAMBDA_NAME'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def invoke_delete_review_lambda(song_id):
    payload = {
        "song_id": song_id,
    }
    lambda_client.invoke(
        FunctionName=os.environ['DELETE_FROM_REVIEWS_LAMBDA_NAME'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def invoke_delete_album_lambda(song_id, album_id):
    payload = {
        "song_id": song_id,
        "album_id": album_id
    }
    lambda_client.invoke(
        FunctionName=os.environ['DELETE_FROM_ALBUM_LAMBDA_NAME'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def invoke_delete_artists_lambda(song_id, artist_ids):
    payload = {
        "song_id": song_id,
        "artist_ids": artist_ids
    }
    lambda_client.invoke(
        FunctionName=os.environ['DELETE_FROM_ARTISTS_LAMBDA_NAME'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )
