import json
import os
import boto3

s3_client = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']
EXPIRATION_TIME = int(os.environ['EXPIRATION_TIME'])


def lambda_handler(event, _context):
    body = json.loads(event['body'])

    content_type = body.get('contentType', 'application/octet-stream')

    allowed_types = ['image/png']
    if content_type not in allowed_types:
        return {
            'statusCode': 400,
            'body': json.dumps({"exception": "Invalid content type"}),
            'headers': {'Content-Type': 'application/json'}
        }

    file_name = body['genreId']
    file_name += '/cover/cover'

    presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": file_name + '.' + content_type.split('/')[1],
            "ContentType": content_type
        },
        ExpiresIn=EXPIRATION_TIME,
        HttpMethod="PUT"
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            "uploadUrl": presigned_url,
        }),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
