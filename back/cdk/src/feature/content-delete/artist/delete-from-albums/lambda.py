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

    artist_id = body.get("artist_id")
    album_ids = body.get("album_ids", [])

    if not artist_id or not album_ids:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "artist_id and album_ids are required"})
        }

    for album_id in album_ids:
        pk = f"ALBUM#{album_id}"
        sk = "METADATA"

        response = table.get_item(Key={"PK": pk, "SK": sk})
        print("Response:", response)
        if not "Item" in response:
            continue
        item = response.get("Item")

        artists = item.get("Artists", [])
        if artist_id in artists:
            del artists[artist_id]

        if len(artists) == 0:
            table.delete_item(Key={"PK": pk, "SK": sk})
        else:
            table.update_item(
                Key={"PK": pk, "SK": sk},
                UpdateExpression="SET Artists = :artists",
                ExpressionAttributeValues={":artists": artists}
            )

    print("Finished")