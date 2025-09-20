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

    song_id = body.get("song_id")
    genre_id = body.get("genre_id")

    if not song_id or not genre_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "song_id and genre_id are required"})
        }

    pk = f"GENRE#{genre_id}"
    sk = "METADATA"

    response = table.get_item(Key={"PK": pk, "SK": sk})
    print("Response:", response)
    if not "Item" in response:
        return None

    item = response.get("Item")
    songs = item.get("Songs", [])
    if song_id in songs:
        del songs[song_id]

    table.update_item(
        Key={"PK": pk, "SK": sk},
        UpdateExpression="SET Songs = :songs",
        ExpressionAttributeValues={":songs": songs}
    )

    print("Finished")