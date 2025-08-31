import json
import os
import boto3

s3_client = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET']
EXPIRATION_TIME = int(os.environ['EXPIRATION_TIME'])


def lambda_handler(event, context):
    body = json.loads(event['body'])

    # Get content type from request, default to image/png
    content_type = body.get('contentType', 'image/png')
    print(content_type)
    # Validate content type
    allowed_types = ['image/png', 'image/x-icon']
    if content_type not in allowed_types:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "Invalid content type"}),
            'headers': {'Content-Type': 'application/json'}
        }

    # Use dynamic file extension
    file_extension = content_type.split('/')[-1]
    file_name = f"{body['genreId']}/icon/icon"

    presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": file_name,
            "ContentType": content_type
        },
        ExpiresIn=EXPIRATION_TIME,
        HttpMethod="PUT"
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            "uploadUrl": presigned_url,
            "contentType": content_type  # Return it so frontend knows what to use
        }),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }