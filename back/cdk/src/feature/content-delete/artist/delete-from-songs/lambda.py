import os
import json
import boto3

dynamo = boto3.resource('dynamodb')
table = dynamo.Table(os.environ['DYNAMO'])
lambda_client = boto3.client('lambda')

DELETE_SONG_LAMBDA = os.environ['DELETE_SONG_LAMBDA_NAME']
def lambda_handler(event, context):
    print("Event:", event)

    if "body" in event:
        body = json.loads(event["body"])
    else:
        body = event

    artist_id = body.get("artist_id")
    song_ids = body.get("song_ids", [])

    if not artist_id or not song_ids:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "artist_id and song_ids are required"})
        }

    for song_id in song_ids:
        pk = f"SONG#{song_id}"
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
            invoke_delete_song_lambda(song_id)
        else:
            table.update_item(
                Key={"PK": pk, "SK": sk},
                UpdateExpression="SET Artists = :artists",
                ExpressionAttributeValues={":artists": artists}
            )

    print("Finished")


def invoke_delete_song_lambda(song_id):
    payload = {
        "resource": "/content-delete/song/{id}",
        "path": f"/content-delete/song/{song_id}",
        "httpMethod": "DELETE",
        "headers": {
            "Authorization": "Bearer FAKE_OR_REAL_TOKEN_IF_NEEDED"
        },
        "pathParameters": {"id": song_id},
        "requestContext": {
            "authorizer": {
                "claims": {
                    "cognito:groups": "Admin",
                    "sub": "fake-user-id"
                }
            }
        }
    }

    lambda_client.invoke(
        FunctionName=DELETE_SONG_LAMBDA,
        InvocationType='Event',
        Payload=json.dumps(payload)
    )
