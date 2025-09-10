import os
import boto3

TABLE_NAME = os.environ['DYNAMO']
table = boto3.resource('dynamodb').Table(TABLE_NAME)

def lambda_handler(event, _context):
    for record in event["Records"]:
        print(record)
        if record["eventName"] != "INSERT":
            continue

        new_item = record["dynamodb"]["NewImage"]
        pk = new_item["PK"]["S"].split("#")[0]
        if pk != 'SONG':
            continue
        song_id = new_item["PK"]["S"].split("#")[1]
        album_dict = new_item.get("Album", {}).get("M")
        if album_dict is not None:
            continue
        genre_dict = new_item.get("Genre", {}).get("M")
        artist_map = new_item.get("Artists", {}).get("M",{})

        song_data = {
            "Id": song_id,
            "Name": new_item["Name"]["S"],
            "CoverPath": new_item["CoverPath"]["S"],
            "AudioPath": new_item["AudioPath"]["S"],
            "ReleaseDate": new_item["ReleaseDate"]["S"],
            "Duration": int(new_item["Duration"]["N"])
        }

        if genre_dict:
            genre_id = genre_dict["Id"]["S"]
            table.update_item(
                Key={"PK": f"GENRE#{genre_id}", "SK": "METADATA"},
                UpdateExpression="SET #songs.#song_id = :song",
                ExpressionAttributeNames={
                    "#songs": "Songs",
                    "#song_id": song_id,
                },
                ExpressionAttributeValues={":song": song_data},
                ReturnValues="UPDATED_NEW"
            )
            # --- Update artists ---
        for artist_id in artist_map.keys():
            print(artist_id)
            table.update_item(
                Key={"PK": f"ARTIST#{artist_id}", "SK": "METADATA"},
                UpdateExpression="SET #songs.#song_id = :song",
                ExpressionAttributeNames={
                    "#songs": "Songs",
                    "#song_id": song_id,
                },
                ExpressionAttributeValues={":song": song_data},
                ReturnValues="UPDATED_NEW"
            )