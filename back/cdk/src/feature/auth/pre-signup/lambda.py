import boto3
import os

client = boto3.client("cognito-idp")

def lambda_handler(event, context):
    user_pool_id = event["userPoolId"]
    username = event["userName"]
    group_name = os.environ["GROUP_NAME"]

    try:
        client.admin_add_user_to_group(
            UserPoolId=user_pool_id,
            Username=username,
            GroupName=group_name
        )
        print(f"User {username} confirmed and added to group {group_name}")
    except Exception as e:
        print(f"Error: {e}")

    return event
