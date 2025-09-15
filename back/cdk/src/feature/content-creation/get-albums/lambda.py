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
from error_handling import with_error_handling

s3_client = boto3.client('s3', region_name=REGION)


@with_error_handling(["Admin"])
def lambda_handler(event, _context):
    artist_ids_to_match = event.get("artistIds", [])
    try:
        db_response = table.scan(
            FilterExpression=Attr("PK").begins_with("ALBUM#") & Attr("SK").begins_with("METADATA")

        )

        items = db_response.get("Items", [])
        filtered_items = []

        for item in items:
            artists_map = item.get('Artists', {})
            for artist_key, artist_value in artists_map.items():
                if artist_value.get('id') in artist_ids_to_match:
                    filtered_items.append(item)
                    break
        responses = [asdict(AlbumResponse(
            id=item['PK'].split('#')[-1],
            title=item.get("Title", ""),
            year=int(item.get("ReleaseDate", "0000-00-00").split('-')[-1]),
            imageUrl=_get_cover_url(item.get('CoverPath') or "sadas"),
            trackNum=len(item.get("Songs", {}))
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
