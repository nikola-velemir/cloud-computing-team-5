import json
import os

import boto3

client = boto3.client('cognito-idp')


def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    email = body.get("email")
    password = body.get("password")
    name = body.get("name")
    lastname = body.get("lastname")
    birthday = body.get("birthday")
    username = body.get("username")

    if not email or not password:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing email or password"})}

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
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "User registered", "userSub": response['UserSub']})
        }
    except client.exceptions.UsernameExistsException:
        return {"statusCode": 400, "body": json.dumps({"error": "User already exists"})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
