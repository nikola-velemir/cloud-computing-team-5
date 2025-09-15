import json
import os
from error_handling import with_error_handling
import boto3

REGION = os.environ['REGION']
s3_client = boto3.client('s3',region_name = REGION)
BUCKET_NAME = os.environ['BUCKET_NAME']
EXPIRATION_TIME = int(os.environ['EXPIRATION_TIME'])


@with_error_handling(["Admin"])
def lambda_handler(event, context):
    body = json.loads(event['body'])
    content_type = body.get('contentType', 'application/octet-stream')
    raw_type = body.get('type')
    if raw_type is None:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }

    file_name = body['songId']
    file_name += f'/{raw_type}/{raw_type}'
    presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": BUCKET_NAME, "Key": file_name + '.' + content_type.split('/')[1], "ContentType": content_type
                },
        ExpiresIn=EXPIRATION_TIME,
        HttpMethod="PUT"
    )

    return {
        'statusCode': 200,
        'body': json.dumps({"uploadUrl": presigned_url}),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    }
