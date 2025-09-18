import json
import os
import boto3
from boto3.dynamodb.conditions import Key
from error_handling import with_error_handling


REGION = os.environ['REGION']
s3_client = boto3.client('s3', region_name=REGION)
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["FEED_TABLE"])
song_bucket = os.environ['SONG_BUCKET']
artist_bucket = os.environ['ARTIST_BUCKET']
album_bucket = os.environ['ALBUM_BUCKET']
genre_bucket = os.environ['GENRE_BUCKET']
EXPIRATION_TIME = int(os.environ['EXPIRATION_TIME'])

BUCKET_MAP = {
    "SONG":   song_bucket,
    "ARTIST": artist_bucket,
    "ALBUM":  album_bucket,
    "GENRE":  genre_bucket,
}

@with_error_handling(["Admin", "AuthenticatedUser"])
def lambda_handler(event, context):
    user_id = event.get('queryStringParameters', {}).get('userId')
    print(user_id)
    if not user_id:
        return {
            'statusCode': 400,
            'body': 'Missing userId query parameter'
        }

    if not user_id:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing PK parameter')
        }

    response = table.query(
        KeyConditionExpression=Key('PK').eq(f'USER#{user_id}'),
    )

    items = response.get('Items', [])
    print(items)
    result = []
    for item in items:
        sk_value = item.get('SK', '')
        parts = sk_value.split('#', 1)
        entity_type = parts[0] if parts else None
        dto = {
            "image": _get_entity_image(item.get('ImagePath'), entity_type),
            "name": item.get('name'),
            "type_entity": entity_type,  # 'GENRE' ili 'ARTIST'
            "id": parts[1] if len(parts) > 1 else None  # 'e79b0d...'
        }
        result.append(dto)
    print(result)
    return {
        "statusCode": 200,
        "body": json.dumps(result),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization"
        }

    }

def _get_entity_image(key: str, entity_type: str) -> str | None:
    if not key or not entity_type:
        return None
    bucket = BUCKET_MAP.get(entity_type.upper())
    if not bucket:
        return None
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=EXPIRATION_TIME,
        )
    except Exception:
        return None
