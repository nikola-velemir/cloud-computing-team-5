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
    genre_ids = body.get("genre_ids", [])

    if not artist_id or not genre_ids:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "artist_id and genre_ids are required"})
        }

    for genre_id in genre_ids:
        pk = f"GENRE#{genre_id}"
        sk = "METADATA"

        response = table.get_item(Key={"PK": pk, "SK": sk})
        print("Response:", response)
        if not "Item" in response:
            continue
        item = response.get("Item")

        artists = item.get("Artists", [])
        if artist_id in artists:
            del artists[artist_id]

        table.update_item(
            Key={"PK": pk, "SK": sk},
            UpdateExpression="SET Artists = :artists",
            ExpressionAttributeValues={":artists": artists}
        )

    print("Finished")