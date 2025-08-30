import json
import os
import boto3

s3_client = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET']
EXPIRATION_TIME = int(os.environ['EXPIRATION_TIME'])

def lambda_handler(event, context):
    body = json.loads(event['body'])
    file_name = body['genreId']
    file_name += '/image/image.ico'
    presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": BUCKET_NAME, "Key": file_name,"ContentType": 'image/x-icon'},
        ExpiresIn=EXPIRATION_TIME,
        HttpMethod="PUT"
    )
    return {
        'statusCode': 200,
        'body': json.dumps({"uploadUrl": presigned_url}),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    }
