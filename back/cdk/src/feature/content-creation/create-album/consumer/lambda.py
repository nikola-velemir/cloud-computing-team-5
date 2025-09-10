import boto3
import os

TABLE_NAME = os.environ['DYNAMO']
table = boto3.resource('dynamodb').Table(TABLE_NAME)

def lambda_handler(event, _context):
    for record in event["Records"]:
        if record["eventName"] != "INSERT":
            continue

        new_item = record["dynamodb"]["NewImage"]
        pk = new_item["PK"]["S"]
        if not pk.startswith("ALBUM#"):
            continue
        print(record)
        album_id = pk.split("#")[1]
        title = new_item["Title"]["S"]
        release_date = new_item["ReleaseDate"]["S"]
        cover_path = new_item["CoverPath"]["S"]

        album_ref = {
            "Id": album_id,
            "Title": title,
            "ReleaseDate": release_date,
            "CoverPath": cover_path,
        }
        print(album_ref)
        artist_map = new_item.get("Artists", {}).get("M", {})
        print(artist_map)
        for artist_id in artist_map.keys():
            table.update_item(
                Key={"PK": f"ARTIST#{artist_id}", "SK": "METADATA"},
                UpdateExpression="SET Albums.#album_id = :album",
                ExpressionAttributeNames={
                    "#album_id": album_id,
                },
                ExpressionAttributeValues={":album": album_ref},
                ReturnValues="UPDATED_NEW"
            )

        genre_map = new_item.get("Genres", {}).get("M", {})
        for genre_id in genre_map.keys():
            table.update_item(
                Key={"PK": f"GENRE#{genre_id}", "SK": "METADATA"},
                UpdateExpression="SET Albums.#album_id = :album",
                ExpressionAttributeNames={
                    "#album_id": album_id,
                },
                ExpressionAttributeValues={":album": album_ref},
                ReturnValues="UPDATED_NEW"
            )
