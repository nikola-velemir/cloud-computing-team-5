import json
import os
import re
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Key

DYNAMO_TABLE = os.environ['FEED_TABLE']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMO_TABLE)
subscribe_map = {
    "INSERT": 200,
    "REMOVE": -400,
}


def lambda_handler(event, context):
    try:
        payload = event
        if payload.get('type') != 'SUBSCRIBE':
            return {'statusCode': 400, 'body': json.dumps({'message': 'Invalid request type'})}

        body = json.loads(payload.get("body", "{}"))
        user = body.get("user") #USER#<ID>
        user_type, user_id = user.split("#")
        content = body.get("content") # ENTITY#<ID>
        content_type, content_id = content.split("#")
        operation = body.get("operation")
        name = body.get("name")
        email = body.get("email")
        imagePath = body.get("imagePath")

        score = subscribe_map.get(operation, 0)
        now = datetime.utcnow().isoformat()

        exist = table.get_item(
            Key={
                "PK": user,
                "SK": content
            }
        )

        if 'Item' in exist:
            score+= exist['Item']['score']
            response = table.update_item(
                Key={
                    "PK": user,
                    "SK": content
                },
                UpdateExpression="SET #s = :score, #updatedAt = :time",
                ExpressionAttributeNames={
                    "#s": "score",
                    "#updatedAt": "updatedAt"
                },
                ExpressionAttributeValues={
                    ":score": score,
                    ":time": now
                }
            )

            print("Updated item:", response["Attributes"])
        else:
            response = table.query(
                KeyConditionExpression=Key("PK").eq(content)
            )

            items = response.get("Items", [])
            if len(items) >= 20:
                min_item = min(items, key=lambda x: x.get("score", float("inf")))
                if min_item.get("score", 0) < score:
                    table.delete_item(
                        Key={
                            "PK": min_item["PK"],
                            "SK": min_item["SK"]
                        }
                    )
                    print(f"Deleted item: {min_item}")

            if imagePath:

                match = re.search(r'https://.*?/(.*?)(?=\?)', imagePath)

                if match:
                    result = match.group(1)
                else:
                    result = ''
            else:
                result = ''
            new_item = {
                "PK": user,
                "SK": content,
                "score": score,
                "updatedAt": now,
                "ImagePath" : result,
                "name": name,
            }

            table.put_item(Item=new_item)
            print(f"Inserted new item: {new_item}")
    except Exception as e:
        print(f"[ERROR] {e}")
        return {"statusCode": 500, "body": str(e)}