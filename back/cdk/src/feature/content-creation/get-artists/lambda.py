import os
from dataclasses import asdict
import json

import boto3
from boto3.dynamodb.conditions import Key

from model.artist import ArtistResponse


TABLE_NAME = os.environ['DYNAMO']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(_event, _context):
    response = table.scan(
        FilterExpression=Key('PK').begins_with("ARTIST#") & Key('SK').eq('METADATA')
    )
    performer_records = response['Items']
    performers = [
        ArtistResponse(id=record.get("PK").split("#")[-1], name=record.get("NAME")) for record in performer_records
    ]
    return {
        'statusCode': 200,
        'body': json.dumps([asdict(p) for p in performers]),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    }
