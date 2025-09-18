
import json
import os
import re
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Key


DYNAMO_TABLE = os.environ['FEED_TABLE']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMO_TABLE)

score_map = {
    "LIKE": 100,
    "DISLIKE": -150,
    "LOVE": 300
}


def lambda_handler(event, context):
    try:
        payload = event
        if payload.get('type') != 'REVIEW':
            return {'statusCode': 400, 'body': json.dumps({'message': 'Invalid request type'})}

        body = json.loads(payload.get("body", "{}"))
        user = body.get("user") #USER#<ID>
        user_type, user_id = user.split("#")
        content = body.get("content") # ENTITY#<ID>
        content_type, content_id = content.split("#")
        operation = body.get("operation")
        rating = body.get("rating")
        imagePath = body.get("imagePath")
        name = body.get("name")

        score = score_map.get(rating, 0)
        now = datetime.utcnow().isoformat()

        exist = table.get_item(
            Key={
                "PK": user,
                "SK": content
            }
        )

        if 'Item' in exist:
            score+= exist['Item']['score']
            table.update_item(
                Key={
                    "PK": user,
                    "SK": content
                },
                UpdateExpression="SET #score = :score, updatedAt = :updatedAt",
                ExpressionAttributeNames={
                    "#score": "score"
                },
                ExpressionAttributeValues={
                    ":score": score,
                    ":updatedAt": now
                }
            )
        else:
            response = table.query(
                KeyConditionExpression=Key("PK").eq(user)
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
                "name":name
            }

            table.put_item(Item=new_item)
            print(f"Inserted new item: {new_item}")



    except Exception as e:
        print(f"[ERROR] {e}")
        return {"statusCode": 500, "body": str(e)}