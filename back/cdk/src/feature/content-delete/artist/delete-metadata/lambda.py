import os
import json
import boto3
from boto3.dynamodb.conditions import Key
from error_handling import with_error_handling

lambda_client = boto3.client('lambda')
dynamodb = boto3.resource('dynamodb')

TABLE_NAME = os.environ['DYNAMO']
dynamo = boto3.resource('dynamodb')
table = dynamo.Table(TABLE_NAME)

@with_error_handling(["Admin"])
def lambda_handler(event, context):
    artist_id = event['pathParameters']['id']
    pk = f"ARTIST#{artist_id}"
    sk = "METADATA"

    response = table.get_item(Key={"PK": pk, "SK": sk})
    item = response.get("Item")
    genre_ids = [g["Id"] for g in item.get("Genres", [])]
    song_ids = [s["Id"] for s in item.get("Songs", {}).values()]
    album_ids = [a["Id"] for a in item.get("Albums", {}).values()]

    invoke_delete_genres_lambda(artist_id, genre_ids)
    invoke_delete_subscriptions_lambda(artist_id)
    invoke_delete_review_lambda(artist_id)
    invoke_delete_album_lambda(artist_id, album_ids)
    claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
    invoke_delete_songs_lambda(artist_id, song_ids,claims)
    invoke_delete_feed_lambda(artist_id)
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


def invoke_delete_genres_lambda(artist_id, genre_ids):
    payload = {
        "artist_id": artist_id,
        "genre_ids": genre_ids
    }
    lambda_client.invoke(
        FunctionName=os.environ['DELETE_FROM_GENRES_LAMBDA_NAME'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def invoke_delete_subscriptions_lambda(artist_id):
    payload = {
        "artist_id": artist_id,
    }
    lambda_client.invoke(
        FunctionName=os.environ['DELETE_FROM_SUBSCRIPTIONS_LAMBDA_NAME'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def invoke_delete_feed_lambda(artist_id):
    payload = {
        "artist_id": artist_id,
    }
    lambda_client.invoke(
        FunctionName=os.environ['DELETE_FROM_FEED_LAMBDA_NAME'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def invoke_delete_review_lambda(artist_id):
    payload = {
        "artist_id": artist_id,
    }
    lambda_client.invoke(
        FunctionName=os.environ['DELETE_FROM_REVIEWS_LAMBDA_NAME'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def invoke_delete_album_lambda(artist_id, album_ids):
    payload = {
        "artist_id": artist_id,
        "album_ids": album_ids
    }
    lambda_client.invoke(
        FunctionName=os.environ['DELETE_FROM_ALBUMS_LAMBDA_NAME'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def invoke_delete_songs_lambda(artist_id, song_ids, claims):
    payload = {
        "artist_id": artist_id,
        "song_ids": song_ids,
        "requestContext": {
            "authorizer": {
                "claims": claims
            }
        }
    }
    lambda_client.invoke(
        FunctionName=os.environ['DELETE_FROM_SONGS_LAMBDA_NAME'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )
