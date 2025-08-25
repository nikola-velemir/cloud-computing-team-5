import base64
import json
import re
import uuid
import boto3
from requests_toolbelt.multipart.decoder import MultipartDecoder
from songify_config.headers import HEADERS

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table  = dynamodb.Table('SongifyDynamo')
BUCKET_NAME = 'albums-bucket-cc5-2025'

def lambda_handler(event,context):
    headers = event.get('headers') or {}
    content_type = headers.get('content-type') or headers.get('Content-Type')
    if not content_type:
        return {
            'statusCode' : 400,
            'body': json.dumps({'message' : 'No header set'}),
            'headers': HEADERS
        }
    
    body_bytes = _decode_body(event=event)
    
    multipart_data = MultipartDecoder(body_bytes, content_type)
    albumName, image_data, image_content_type, artist_ids, release_date = _parsed_body(multipart_data)

    if not albumName:
        return{
            'statusCode':400,
            'body': json.dumps({'message' : 'Album name missing'}),
            'headers':HEADERS
        }
    
    image_url = None;
    albumId = str(uuid.uuid4())
    if image_data:
        imageKey = f'albums/{albumId}/cover/cover.jpg'
        s3.put_object(
            Bucket = BUCKET_NAME,
            Key = imageKey,
            Body = image_data,
            ContentType = image_content_type
        )
        image_url = f'https://{BUCKET_NAME}.s3.amazonaws.com/{imageKey}',

    table.put_item(
        Item = {
            'PK' : f'ALBUM#{albumId}',
            "SK" : 'METADATA',
            'Title':albumName,
            'ArtistIds':artist_ids,
            'ImageUrl': image_url or '',
            'RelaseDate':release_date
        }
    )

    return {
        'statusCode':201,
        'body':json.dumps({'albumId':albumId}),
        'headers': HEADERS
    }
def _parsed_body(multipart_data):
    albumName = ''
    image_data = None
    image_content_type = None
    artist_ids = []
    release_date :str= ''
    for part in multipart_data.parts:        
        cd = part.headers[b'Content-Disposition'].decode()
        field_name = get_field_name(cd)

        if field_name=='albumName':
            albumName = part.text

        elif field_name =='albumImage':
            image_data = part.content
            image_content_type = part.headers.get(b'Content-Type', b'image/jpeg').decode()
        elif field_name == 'artistIds':
            artist_ids_str :str = part.text
            artist_ids = json.loads(artist_ids_str)
        elif field_name == 'releaseDate':
            release_date:str = part.text

    return albumName, image_data, image_content_type, artist_ids, release_date


def get_field_name(content_disposition: str) -> str:
    match = re.search(r'name="([^"]+)"', content_disposition)
    if match:
        return match.group(1)
    return ''

def _decode_body(event):
    if event.get('isBase64Encoded',False):
        body_bytes = base64.b64decode(event['body'])
    else:
        body_bytes = event['body'].encode("utf-8")
    return body_bytes
