import json
import os
import uuid
from dataclasses import asdict
from datetime import datetime

import boto3
from error_handling import with_error_handling
from model.artist_model import *

lambda_client = boto3.client('lambda')
TABLE_NAME = os.environ['DYNAMO']
dynamo = boto3.resource('dynamodb')
table = dynamo.Table(TABLE_NAME)

# body : {
#   "name" : "artist name",
#   "biography" : "my bio",
#   "genres_id" : [1,2,3],
# }
@with_error_handling(["Admin"])
def lambda_handler(event, context):
    if "body" in event:
        body = json.loads(event["body"])
    else:
        body = event
    artist_id = body['id']
    genre_ids = body['genres_id']
    name = body['name']
    biography = body['biography']

    if not genre_ids:
        return {"statusCode": 400, "body": json.dumps({"error": "No genres provided"})}

    if not name:
        return {"statusCode": 400, "body": json.dumps({"error": "No name provided"})}

    if not biography:
        return {"statusCode": 400, "body": json.dumps({"error": "No biography provided"})}

    old_artist = table.get_item(Key={
        'PK': f'ARTIST#{artist_id}',
        'SK': f'METADATA'
    }).get("Item")
    old_genres = old_artist.get("Genres", [])
    old_ids = {g["Id"] for g in old_genres}
    keys = [{'PK': f'GENRE#{gid}', 'SK': "METADATA"} for gid in genre_ids]
    resp = dynamo.meta.client.batch_get_item(
        RequestItems={
            TABLE_NAME: {"Keys": keys},
        }
    )
    found_items = resp["Responses"].get(TABLE_NAME, [])
    found_genres = []
    for item in found_items:
        found_genres.append(_map_genre_to_dto(item))

    print(found_genres)
    found_ids = {item["PK"].replace("GENRE#", "") for item in found_items}

    missing = [gid for gid in genre_ids if str(gid) not in found_ids]
    if missing:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps({"error": f"Genres not found: {missing}"})
        }

    old_artist["Name"] = name
    old_artist["Biography"] = biography
    old_artist["Genres"] = old_artist["Genres"] = [asdict(g) for g in found_genres]


    table.put_item(Item=old_artist)


    new_ids = {g.Id for g in found_genres}
    to_add = list(new_ids - old_ids)
    to_update = list(new_ids & old_ids)
    to_remove = list(old_ids - new_ids)

    albums = old_artist.get("Albums", {})
    songs = old_artist.get("Songs", {})

    album_ids = list(albums.keys())
    song_ids = list(songs.keys())

    _invoke_add_artist_to_genres(artist_id, name,biography, to_add)
    # _invoke_remove_artist_from_genres(artist_id, to_remove)
    # _invoke_update_artist_in_albums(artist_id, name, album_ids)
    _invoke_update_artist_in_feed(artist_id, name)
    # _invoke_update_artist_in_genres(artist_id, name,biography, to_update)
    _invoke_update_artist_in_reviews(artist_id, name)
    # _invoke_update_artist_in_songs(artist_id, name, song_ids)
    _invoke_update_artist_in_subscriptions(artist_id, name)

    return {
        "statusCode": 201,
        "headers": {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    },
        "body": json.dumps({"message": "Artist created", "genreId": artist_id, })
    }

def _map_genre_to_dto(item):
    return GenreDTO(
        Id=item['PK'].replace("GENRE#", ""),
        Name=item['Name'],
        Image=item['CoverPath'],
    )

def _invoke_add_artist_to_genres(artist_id, artist_name,artist_bio, new_genre_ids):
    payload = {
        "artist_id": artist_id,
        "artist_name": artist_name,
        "artist_bio": artist_bio,
        "genre_ids": new_genre_ids,
    }
    lambda_client.invoke(
        FunctionName=os.environ['ADD_ARTIST_TO_GENRES'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def _invoke_remove_artist_from_genres(artist_id, old_genre_ids):
    payload = {
        "artist_id": artist_id,
        "genre_ids": old_genre_ids,
    }
    lambda_client.invoke(
        FunctionName=os.environ['REMOVE_ARTIST_FROM_GENRES'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def _invoke_update_artist_in_albums(artist_id, artist_name, album_ids):
    payload = {
        "artist_id": artist_id,
        "artist_name": artist_name,
        "album_ids": album_ids,
    }
    lambda_client.invoke(
        FunctionName=os.environ['UPDATE_ARTIST_IN_ALBUMS'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def _invoke_update_artist_in_feed(artist_id, artist_name,):
    payload = {
        "artist_id": artist_id,
        "artist_name": artist_name,
    }
    lambda_client.invoke(
        FunctionName=os.environ['UPDATE_ARTIST_IN_FEED'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def _invoke_update_artist_in_genres(artist_id, artist_name,artist_bio,  genre_ids):
    payload = {
        "artist_id": artist_id,
        "artist_name": artist_name,
        "artist_bio": artist_bio,
        "genre_ids": genre_ids,
    }
    lambda_client.invoke(
        FunctionName=os.environ['UPDATE_ARTIST_IN_GENRES'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def _invoke_update_artist_in_reviews(artist_id, artist_name):
    payload = {
        "artist_id": artist_id,
        "artist_name": artist_name,
    }
    lambda_client.invoke(
        FunctionName=os.environ['UPDATE_ARTIST_IN_REVIEWS'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def _invoke_update_artist_in_songs(artist_id, artist_name, song_ids):
    payload = {
        "artist_id": artist_id,
        "artist_name": artist_name,
        "song_ids": song_ids
    }
    lambda_client.invoke(
        FunctionName=os.environ['UPDATE_ARTIST_IN_SONGS'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )

def _invoke_update_artist_in_subscriptions(artist_id, artist_name):
    payload = {
        "artist_id": artist_id,
        "artist_name": artist_name,
    }
    lambda_client.invoke(
        FunctionName=os.environ['UPDATE_ARTIST_IN_SUBSCRIPTIONS'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )