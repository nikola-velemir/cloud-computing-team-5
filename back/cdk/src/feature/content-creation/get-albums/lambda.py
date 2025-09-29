import os
from dataclasses import asdict
import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from error_handling import with_error_handling
from model.album import AlbumResponse

REGION = os.environ['REGION']
EXPIRATION_TIME = int(os.environ.get("EXPIRATION_TIME"))
BUCKET_NAME = os.environ['BUCKET']
TABLE_NAME = os.environ['DYNAMO']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

s3_client = boto3.client('s3', region_name=REGION)


@with_error_handling(["Admin"])
def lambda_handler(event, _context):
    body = json.loads(event["body"])
    artist_ids_to_match = body.get("artistIds", [])
    print(artist_ids_to_match)
    key_condition = Key("EntityType").eq("ALBUM") & Key("SK").eq("METADATA")
    try:
        db_response = table.query(
            IndexName="EntitiesIndex",
            KeyConditionExpression=key_condition,
        )

        items = db_response.get("Items", [])
        print(items)
        filtered_items = []

        for item in items:
            artists_map = item.get('Artists', {})
            for artist_key, artist_value in artists_map.items():
                if artist_value.get('Id') in artist_ids_to_match:
                    filtered_items.append(item)
                    break
        responses = []
        for item in filtered_items:
            print(item)
            cover_path = item.get('CoverPath')
            responses.append(asdict(AlbumResponse(
                id=item['PK'].split('#')[-1],
                title=item.get("Title", ""),
                year=int(item.get("ReleaseDate", "01-01-0000").split('-')[-1]),
                imageUrl=_get_cover_url(cover_path) if cover_path else None,
                trackNum=len(item.get("Songs", {}))
            )))

        return {
            'statusCode': 200,
            'body': json.dumps(responses),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }

    except Exception as e:
        print(e)
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
