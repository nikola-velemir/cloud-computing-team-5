import json
import os
import boto3

STEP_FUNCTION_ARN = os.environ["STEP_FUNCTION_ARN"]

sfn = boto3.client("stepfunctions")

def lambda_handler(event, context):
    for record in event.get("Records", []):
        if record["eventName"] != "INSERT":
            continue

        new_image = record["dynamodb"]["NewImage"]
        pk = new_image["PK"]["S"]

        if pk.startswith("ALBUM#"):
            type_ = "ALBUM"
        elif pk.startswith("ARTIST#"):
            type_ = "ARTIST"
        elif pk.startswith("SONG#"):
            type_ = "SONG"
        else:
            continue

        payload = {
            "type": type_,
            "dynamodb": new_image
        }

        sfn.start_execution(
            stateMachineArn=STEP_FUNCTION_ARN,
            input=json.dumps(payload)
        )

    return {"statusCode": 200, "body": "Step Functions triggered"}
