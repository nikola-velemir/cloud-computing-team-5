import json
import os

import boto3

s3_client = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']
EXPIRATION_TIME = int(os.environ['EXPIRATION_TIME'])
def lambda_handler(event, context):
    body = json.loads(event['body'])
    file_name = body['file_name']
    presigned_url = s3_client.generate_presigned_url('put_object', Params={
        'Bucket': BUCKET_NAME,
        'Key': file_name,
        "Expires": EXPIRATION_TIME
    }, HttpMethod="put")
    return {
        'statusCode': 307,
        'headers':{
            'Location': presigned_url
        }
    }