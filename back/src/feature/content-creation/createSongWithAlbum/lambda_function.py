import base64
import json
import uuid
import boto3
from requests_toolbelt.multipart.decoder import MultipartDecoder
from songify_config.headers import HEADERS
import re


s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SongifyDynamo')
BUCKET_NAME = 'songs-bucket-cc5-2025'

def lambda_handler(event,context):
    headers = event.get('headers') or {}
    content_type = headers.get('content-type') or headers.get('Content-Type')
    if not content_type:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Missing Content-Type header"})
        }
    
    body_bytes = _decode_body(event=event)

    multipart_data = MultipartDecoder(body_bytes, content_type)

    parsed_body = _parse_body(multipart_data)
    
    song_id = str(uuid.uuid4())
    image_key = f'songs/{song_id}/cover/cover.jpg'
    audio_key = f'songs/{song_id}/audio/audio.mp3'

    if parsed_body['image_data']:
        s3.put_object(
            Bucket = BUCKET_NAME,
            Key = image_key,
            Body = parsed_body['image_data'],
            ContentType=parsed_body['image_content_type']
        )
    if parsed_body['audio_data']:
        s3.put_object(
            Bucket = BUCKET_NAME,
            Key = audio_key,
            Body = parsed_body['audio_data'],
            ContentType=parsed_body['audio_content_type']
        )
    
    table.put_item(
        Item = {
            'PK' : f"SONG#{song_id}",
            "SK" : f'METADATA',
            "Name" : parsed_body['song_name'],
            "ImageUrl" : f'https://{BUCKET_NAME}.s3.amazonaws.com/{image_key}',
            "AudioUrl" :  f'https://{BUCKET_NAME}.s3.amazonaws.com/{audio_key}'
        }
    )
    return {
        "statusCode": 201,
        "body": json.dumps({
            "songId": song_id,
            "songName": parsed_body["song_name"],
            "genreId": parsed_body["genre_id"]
        }),
        "headers":HEADERS
    }


def _parse_body(multipart_data):
    song_name = ''
    genre_id = ''
    image_data = None
    image_content_type = None
    audio_data =None
    audio_content_type = None
    artists = []

    for part in multipart_data.parts:
        cd = part.headers[b'Content-Disposition'].decode()
        field_name = get_field_name(cd)

        if field_name == 'songName':
            song_name = part.text
        elif field_name == 'genreId':
            genre_id = part.text
        elif field_name == 'image':
            image_data = part.content
            image_content_type = part.headers.get(b'Content-Type', b'image/jpeg').decode()
        elif field_name == 'audio':
            audio_data = part.content
            audio_content_type = part.headers.get(b'Content-Type', b'audio/mpeg').decode()
        elif field_name == 'artists':
            artists = json.loads(part.text)

    
    return {
        'song_name':song_name,
        'genre_id':genre_id,
        'image_data':image_data,
        'image_content_type':image_content_type,
        'audio_data' : audio_data,
        'audio_content_type' : audio_content_type,
        'artists' : artists
    }



def _decode_body(event):
    if event.get('isBase64Encoded',False):
        body_bytes = base64.b64decode(event['body'])
    else:
        body_bytes = event['body'].encode("utf-8")
    return body_bytes


def get_field_name(content_disposition: str) -> str:
    match = re.search(r'name="([^"]+)"', content_disposition)
    if match:
        return match.group(1)
    return ''
