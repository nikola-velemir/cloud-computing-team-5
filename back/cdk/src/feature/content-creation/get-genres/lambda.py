import json
import os

from model.genre import Genre
import boto3
from dataclasses import asdict

TABLE_NAME = os.environ['DYNAMO']
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    db_response = table.scan(
        FilterExpression="begins_with(PK, :genre)",
        ExpressionAttributeValues={
            ":genre": "GENRE#"
        }
    )
    items = db_response.get("Items", [])

    responses = [
        asdict(Genre(id=item["PK"].split("#")[1],
                     name=item.get("Name"))
               ) for item in items]

    return {
        'statusCode': 200,
        'body': json.dumps(responses),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    }
