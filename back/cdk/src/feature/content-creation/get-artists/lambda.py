import os
from dataclasses import asdict
import json

import boto3
from boto3.dynamodb.conditions import Key

from model.artist import ArtistResponse

REGION = os.environ['REGION']
EXPIRATION_TIME = int(os.environ.get("EXPIRATION_TIME"))
BUCKET_NAME = os.environ['BUCKET']
TABLE_NAME = os.environ['DYNAMO']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

s3_client = boto3.client('s3', region_name=REGION)


def lambda_handler(_event, _context):
    response = table.scan(
        FilterExpression=Key('PK').begins_with("ARTIST#") & Key('SK').eq('METADATA')
    )
    performer_records = response['Items']
    performers = [
        ArtistResponse(
            id=record.get("PK").split("#")[-1],
            name=record.get("Name") or record.get("FirstName", "") + " " + record.get("LastName", ""),
            imageUrl=_get_cover_url(record.get("ImagePath", "daa"))
        ) for record in performer_records
    ]
    return {
        'statusCode': 200,
        'body': json.dumps([asdict(p) for p in performers]),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    }


def _get_cover_url(cover_path: str) -> str:
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": cover_path},
            ExpiresIn=EXPIRATION_TIME
        )
    except Exception as e:
        print("Error:", e)
        return None
