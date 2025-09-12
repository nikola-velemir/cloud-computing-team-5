import os
import json
import boto3
from boto3.dynamodb.conditions import Key
from dataclasses import asdict

from model.genres_response import Genre,GenresResponse

TABLE_NAME = os.environ['DYNAMO']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    try:
        query_params = {
            "IndexName": "EntitiesIndex",
            "KeyConditionExpression": Key("EntityType").eq("GENRE") & Key("SK").eq("METADATA"),
        }

        db_response = table.query(**query_params)

        items = db_response.get("Items", [])

        genres = [
            Genre(
                id=item['PK'].split('#')[1],
                name=item.get("Name", ""),
            )
            for item in items
        ]

        response = GenresResponse(
            genres=genres,
        )
        return {
            "statusCode": 200,
            "body": json.dumps(asdict(response)),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }
