import json
import os

from boto3.dynamodb.conditions import Key
from error_handling import with_error_handling

import boto3

SUBSCRIPTION_TABLE = os.environ["SUBSCRIPTION_TABLE"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(SUBSCRIPTION_TABLE)


@with_error_handling(["Admin", "AuthenticatedUser"])
def lambda_handler(event, context):
    user_id = None

    if event.get("queryStringParameters"):
        user_id = event["queryStringParameters"].get("userId")

    if not user_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Missing userId"})
        }

    resp = table.query(
        IndexName="UserIndex",
        KeyConditionExpression=Key("SK").eq(f'USER#{user_id}')
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp.get("Items", [])),
        "headers": {"Content-Type": "application/json"}
    }