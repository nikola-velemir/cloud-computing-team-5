import json
import os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
REGION = os.environ['REGION']
ses = boto3.client('ses', region_name=REGION)
sqs = boto3.client('sqs')

SUBSCRIPTION_TABLE = os.environ["SUBSCRIPTION_TABLE"]
FEED_SQS_URL = os.environ['FEED_SQS_URL']


def lambda_handler(event, context):
    try:


        msg_type = event.get('type')
        if msg_type != 'ALBUM':
            return {"statusCode": 400, "body": "Not an ALBUM event"}
        album = event.get('album')
        genres = event.get('genres')

        if not genres or not album:
            return {"statusCode": 400, "body": "Missing album or genres"}

        table = dynamodb.Table(SUBSCRIPTION_TABLE)

        for genre in genres:
            genre_id = genre.get('Id')
            if not genre_id:
                continue

            response = table.query(
                KeyConditionExpression=Key('PK').eq(f'GENRE#{genre_id}')
            )
            subscribers = response.get('Items', [])

            for sub in subscribers:
                email = sub.get('Email')
                if not email:
                    continue

                body = {
                    "user": sub["SK"],
                    "content": f'ALBUM#{album.get("id")}',
                    "name": album.get('Name'),
                    "imagePath": album.get('CoverPath'),
                }

                sqs.send_message(
                    QueueUrl=FEED_SQS_URL,
                    MessageBody=json.dumps({
                        "type": "NEW_ENTITY",
                        "body": json.dumps(body)
                    })
                )
                print(f"A new album '{album.get('Name')}' has been added to the feed sqs")

                ses.send_email(
                    Source="songifytest@gmail.com",
                    Destination={"ToAddresses": [email]},
                    Message={
                        "Subject": {"Data": f"New album in genre {genre.get('Name')}!"},
                        "Body": {
                            "Text": {
                                "Data": f"A new album '{album.get('Name')}' has been added to the genre '{genre.get('Name')}'."
                            }
                        }
                    }
                )
            print(
                f"[INFO] Sent notifications for album '{album.get('Name')}' "
                f"to {len(subscribers)} subscribers of genre '{genre.get('Name')}'"
            )

    except Exception as e:
        print(f"[ERROR] {e}")
        return {"statusCode": 500, "body": str(e)}

    return {"statusCode": 200, "body": "Processed message"}
