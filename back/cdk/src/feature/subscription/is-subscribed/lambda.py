import os
import json
import boto3
from error_handling import with_error_handling


SUBSCRIPTION_TABLE = os.environ.get("SUBSCRIPTION_TABLE")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(SUBSCRIPTION_TABLE)

@with_error_handling(["Admin", "AuthenticatedUser"])
def lambda_handler(event, _context):
    params = event.get("queryStringParameters") or {}
    user_id = params.get("userId")
    entity_type = params.get("entityType")
    content_id = params.get("contentId")

    if not user_id or not entity_type or not content_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing required parameters"})
        }

    pk = f"{entity_type}#{content_id}"
    sk = f"USER#{user_id}"
    try:
        response = table.get_item(
            Key={
                "PK": pk,
                "SK": sk
            }
        )
        exists = "Item" in response
        if exists:
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(True)
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }
