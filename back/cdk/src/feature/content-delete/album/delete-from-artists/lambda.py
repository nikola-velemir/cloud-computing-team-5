import os
import json
import boto3

dynamo = boto3.resource('dynamodb')
table = dynamo.Table(os.environ['DYNAMO'])


def lambda_handler(event, context):
    print("Event:", event)

    if "body" in event:
        body = json.loads(event["body"])
    else:
        body = event

    album_id = body.get("album_id")
    artist_ids = body.get("artist_ids")

    if not album_id or not artist_ids:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "album_id and artist_ids are required"})
        }

    for artist_id in artist_ids:
        pk = f"ARTIST#{artist_id}"
        sk = "METADATA"

        response = table.get_item(Key={"PK": pk, "SK": sk})
        print("Response:", response)
        if not "Item" in response:
            continue
        item = response.get("Item")

        albums = item.get("Albums", [])
        if album_id in albums:
            del albums[album_id]

        table.update_item(
            Key={"PK": pk, "SK": sk},
            UpdateExpression="SET Albums = :albums",
            ExpressionAttributeValues={":albums": albums}
        )


    print("Finished")