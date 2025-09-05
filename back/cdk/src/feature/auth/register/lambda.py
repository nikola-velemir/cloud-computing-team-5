import json
import os

import boto3

client = boto3.client('cognito-idp')


import json
import os
import boto3

client = boto3.client('cognito-idp')


def build_response(status_code, body):
    """
    Helper funkcija da svi odgovori imaju CORS header.
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    if event.get("httpMethod") == "OPTIONS":
        return build_response(200, {"message": "CORS preflight OK"})

    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return build_response(400, {"error": "Invalid JSON body"})

    email = body.get("email")
    password = body.get("password")
    name = body.get("name")
    lastname = body.get("lastname")
    birthday = body.get("birthday")
    username = body.get("username")

    if not email or not password or not name or not lastname or not birthday or not username:
        return build_response(400, {"error": "Missing required fields"})

    try:
        response = client.sign_up(
            ClientId=os.environ["CLIENT_ID"],
            Username=email,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email},
                {"Name": "name", "Value": name},
                {"Name": "family_name", "Value": lastname},
                {"Name": "birthdate", "Value": birthday},
                {"Name": "preferred_username", "Value": username}
            ]
        )

        client.admin_confirm_sign_up(
            UserPoolId=os.environ["USER_POOL_ID"],
            Username=email
        )

        return build_response(200, {"message": "User registered", "userSub": response['UserSub']})

    except client.exceptions.UsernameExistsException:
        return build_response(400, {"error": "User already exists"})
    except Exception as e:
        return build_response(500, {"error": str(e)})
