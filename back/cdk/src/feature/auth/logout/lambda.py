import boto3
import json

client = boto3.client("cognito-idp")

def lambda_handler(event, context):
    token = event["headers"].get("Authorization")
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing or invalid Authorization header"})
        }

    try:
        client.global_sign_out(AccessToken=token)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Successfully logged out"})
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }
