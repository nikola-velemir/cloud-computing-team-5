import os
from dataclasses import asdict
import json
import boto3
from boto3.dynamodb.conditions import Attr

from model.album import AlbumResponse

REGION = os.environ['REGION']
EXPIRATION_TIME = int(os.environ.get("EXPIRATION_TIME"))
BUCKET_NAME = os.environ['BUCKET']
TABLE_NAME = os.environ['DYNAMO']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

s3_client = boto3.client('s3',region_name = REGION)

def lambda_handler(_event, _context):
    try:
        db_response = table.scan(
            FilterExpression=Attr("PK").begins_with("ALBUM#") & Attr("SK").begins_with("METADATA")

        )

        items = db_response.get("Items", [])

        responses = [asdict(AlbumResponse(
            id=item['PK'].split('#')[1],
            title=item.get("Title", ""),
            year=int(item.get("ReleaseDate", "0000-00-00").split('-')[2]),
            artistIds=item.get("ArtistIds", []),
            imageUrl=_get_cover_url(item['PK'].split('#')[1], item['ImageType']),
        )) for item in items]

        return {
            'statusCode': 200,
            'body': json.dumps(responses),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'exception': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }


def _get_cover_url(album_id: str,image_type: str) -> str:
    key = f'{album_id}/cover/cover.{image_type}'
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": key},
            ExpiresIn=EXPIRATION_TIME
        )
    except Exception as e:
        print("Error:", e)
        return None
