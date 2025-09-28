import json
import os

import boto3
from botocore.exceptions import ClientError
from error_handling import with_error_handling

SUBSCRIPTION_TABLE = os.environ["SUBSCRIPTION_TABLE"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(SUBSCRIPTION_TABLE)

@with_error_handling(["Admin", "AuthenticatedUser"])
def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        user_id = body.get("userId")
        entity_type = body.get("entityType")
        content_id = body.get("contentId")

        if not all([user_id, entity_type, content_id]):
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(False)
            }

        pk = f"{entity_type}#{content_id}"
        sk = f"USER#{user_id}"

        table.delete_item(
            Key={
                "PK": pk,
                "SK": sk
            },
            ConditionExpression="attribute_exists(PK) AND attribute_exists(SK)"
        )

        return {
            "statusCode": 204,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }


    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(False)
            }
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(False)
        }

    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(False)
        }