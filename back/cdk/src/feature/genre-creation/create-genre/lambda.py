import json
import uuid
import base64
from dataclasses import asdict
import boto3
from model.genre import Genre
from requests_toolbelt.multipart.decoder import MultipartDecoder
import mimetypes

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SongifyDynamo')
bucket_name = 'genre-bucket-cc52025'


def lambda_handler(event, context):
    headers = event.get('headers') or {}
    content_type = headers.get('content-type') or headers.get('Content-Type')
    if not content_type:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Missing Content-Type header"})
        }

    if event.get('isBase64Encoded', False):
        body_bytes = base64.b64decode(event['body'])
    else:
        body_bytes = event['body'].encode("utf-8")

    multipart_data = MultipartDecoder(body_bytes, content_type)

    genre_name = ''
    image_data = None
    image_content_type = None

    for part in multipart_data.parts:
        cd = part.headers[b'Content-Disposition'].decode()
        if 'name="name"' in cd:
            genre_name = part.text
        elif 'name="image"' in cd:
            image_data = part.content
            image_content_type = part.headers.get(b'Content-Type', b'image/jpeg').decode()

    genre_id = str(uuid.uuid4())
    image_url = ""

    if image_data:
        # derive extension from mime
        file_ext = mimetypes.guess_extension(image_content_type) or ".jpg"
        image_key = f'genres/{genre_id}{file_ext}'

        s3.put_object(
            Bucket=bucket_name,
            Key=image_key,
            Body=image_data,
            ContentType=image_content_type
        )
        image_url = f'https://{bucket_name}.s3.amazonaws.com/{image_key}'

        genre = Genre(PK=f'GENRE#{genre_id}', SK="METADATA", Name=genre_name, ImageUrl=image_url)
        table.put_item(Item=asdict(genre))

    return {
        "statusCode": 201,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"message": "Genre created", "genreId": genre_id, "imageURL": image_url})
    }