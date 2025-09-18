import json
import os
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Key

DYNAMO_TABLE = os.environ['FEED_TABLE']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMO_TABLE)

# New entity
def lambda_handler(event, context):
    try:
        payload = event
        if payload.get('type') != 'NEW_ENTITY':
            return {'statusCode': 400, 'body': json.dumps({'message': 'Invalid request type'})}

        body = json.loads(payload.get("body", "{}"))
        user = body.get("user")  # USER#<ID>
        user_type, user_id = user.split("#")
        content = body.get("content")  # ENTITY#<ID>
        content_type, content_id = content.split("#")
        name = body.get("name")
        image_path = body.get("imagePath")

        score = 0
        now = datetime.utcnow().isoformat()

        response = table.query(
            KeyConditionExpression=Key("PK").eq(user)
        )
        items = response.get("Items", [])
        if len(items) >= 20:
            min_item = min(items, key=lambda x: x.get("score", float("inf")))
            table.delete_item(
                Key={
                    "PK": min_item["PK"],
                    "SK": min_item["SK"]
                }
            )
            print(f"Deleted item: {min_item}")

        new_item = {
            "PK": user,
            "SK": content,
            "score": score,
            "updatedAt": now,
            "name": name,
            "ImagePath": image_path,
        }

        table.put_item(Item=new_item)
        print(f"Inserted new item: {new_item}")

    except Exception as e:
        print(f"[ERROR] {e}")
        return {"statusCode": 500, "body": str(e)}