import boto3
import os
import json
import jwt

client = boto3.client("cognito-idp")

def lambda_handler(event, context):
    body = json.loads(event["body"])
    email = body["email"]
    password = body["password"]

    response = client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": email,
            "PASSWORD": password
        },
        ClientId=os.environ["CLIENT_ID"]
    )

    auth_result = response["AuthenticationResult"]
    id_token = auth_result["IdToken"]
    access_token = auth_result["AccessToken"]

    payload = jwt.decode(id_token, options={"verify_signature": False})
    groups = payload.get("cognito:groups", [])

    response = client.get_user(AccessToken=access_token)

    attributes = {attr["Name"]: attr["Value"] for attr in response["UserAttributes"]}

    user_info = {
        "userId": attributes.get("sub"),
        "email": attributes.get("email"),
        "fullName": attributes.get("name") + attributes.get("family_name"),
        "username": attributes.get("preferred_username"),
        "birthday": attributes.get("birthdate"),
        "role" : groups[0] if groups else None,
    }

    return {
        "statusCode": 200,
        "headers": {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    },
        "body": json.dumps({
            "access_token": access_token,
            "id_token":id_token,
            "refresh_token": auth_result["RefreshToken"],
            "groups": groups,
            "user": user_info
        })
    }
