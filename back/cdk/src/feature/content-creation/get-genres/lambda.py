import json
import os

from aws_cdk.aws_kms import Key
from error_handling import with_error_handling
from model.genre import Genre
import boto3
from dataclasses import asdict

REGION = os.environ['REGION']
TABLE_NAME = os.environ['DYNAMO']
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)
BUCKET_NAME = os.environ['BUCKET']
EXPIRATION_TIME = int(os.environ['EXPIRATION_TIME'])

s3_client = boto3.client('s3',region_name = REGION)

@with_error_handling(["Admin"])
def lambda_handler(_event, _context):
    key_condition = Key("EntityType").eq("Genre") & Key("SK").eq("METADATA")
    db_response = table.query(
        IndexName="EntitiesIndex",
        KeyConditionExpression=key_condition,
    )
    items = db_response.get("Items", [])

    responses = []
    for item in items:
        responses.append(asdict(Genre(id=item["PK"].split("#")[1],
                                      name=item.get("Name"),
                                      url=_get_cover_url(item)
                                )))

    return {
        'statusCode': 200,
        'body': json.dumps(responses),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    }


def _get_cover_url(item):

    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": item.get("CoverPath") or 'vv'},
        ExpiresIn=EXPIRATION_TIME
    )
