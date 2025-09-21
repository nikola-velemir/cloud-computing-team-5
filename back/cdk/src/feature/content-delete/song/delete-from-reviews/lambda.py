import os
import json
import boto3
from boto3.dynamodb.conditions import Key

dynamo = boto3.resource("dynamodb")
table = dynamo.Table(os.environ["DYNAMO"])

def lambda_handler(event, context):
    print("Event:", event)

    if "body" in event:
        body = json.loads(event["body"])
    else:
        body = event

    song_id = body.get("song_id")

    if not song_id:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PUT,DELETE",
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
            },
            "body": json.dumps({"error": "artist_id is required"}),
        }

    pk = f"SONG#{song_id}"
    last_evaluated_key = None
    gsi_name = "ReviewContentIndex"

    with table.batch_writer() as batch:
        while True:
            query_args = {
                "IndexName": gsi_name,
                "KeyConditionExpression": Key("Content").eq(pk),
                "Limit": 20
            }
            if last_evaluated_key:
                query_args["ExclusiveStartKey"] = last_evaluated_key

            response = table.query(**query_args)

            items = response.get("Items", [])

            for item in items:
                batch.delete_item(Key={"User": item["User"], "Content": item["Content"]})

            last_evaluated_key = response.get("LastEvaluatedKey")
            if not last_evaluated_key:
                break

    print("Finished")
