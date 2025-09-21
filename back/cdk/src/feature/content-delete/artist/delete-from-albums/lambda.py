import os
import json
import boto3

dynamo = boto3.resource('dynamodb')
table = dynamo.Table(os.environ['DYNAMO'])
lambda_client = boto3.client('lambda')
DELETE_ALBUM_LAMBDA = os.environ['DELETE_ALBUM_LAMBDA_NAME']


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
            invoke_delete_album_lambda(album_id)
        else:
            table.update_item(
                Key={"PK": pk, "SK": sk},
                UpdateExpression="SET Artists = :artists",
                ExpressionAttributeValues={":artists": artists}
            )

    print("Finished")

def invoke_delete_album_lambda(album_id):
    payload = {
        "resource": "/content-delete/song/{id}",
        "path": f"/content-delete/album/{album_id}",
        "httpMethod": "DELETE",
        "headers": {
            "Authorization": "Bearer FAKE_OR_REAL_TOKEN_IF_NEEDED"
        },
        "pathParameters": {"id": album_id},
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
        FunctionName=DELETE_ALBUM_LAMBDA,
        InvocationType='Event',
        Payload=json.dumps(payload)
    )
