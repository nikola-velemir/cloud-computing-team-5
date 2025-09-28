import json
import os
import boto3
from datetime import datetime
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
        user_email = body.get("userEmail")
        entity_type = body.get("entityType")
        content_id = body.get("contentId")
        name = body.get("name")
        coverPath = body.get("coverPath")

        if not all([user_id, user_email, entity_type, content_id]):
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

        item = {
            "PK": pk,
            "SK": sk,
            "Email": user_email,
            "CreatedAt":datetime.utcnow().isoformat(),
            "Name" : name,
            "CoverPath": coverPath,
        }

        table.put_item(
            Item=item,
            ConditionExpression="attribute_not_exists(PK) AND attribute_not_exists(SK)"
        )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(True)
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
