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
        if msg_type != 'ARTIST':
            return {"statusCode": 400, "body": "Not an ARTIST event"}

        artist = event.get('artist')
        genres = event.get('genres')

        if not genres or not artist:
            return {"statusCode": 400, "body": "Missing artist or genres"}

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
                    "user": f'ARTIST#{artist.get("PK")}',
                    "content": f'GENRE#{genre_id}',
                    "name": artist.get('Name'),
                    "imagePath" : artist.get('CoverPath'),
                }

                sqs.send_message(
                        QueueUrl=FEED_SQS_URL,
                        MessageBody=json.dumps({
                            "type": "NEW_ENTITY",
                            "body": json.dumps(body)
                        })
                    )
                print(f"A new artist '{artist.get('Name')}' has been added to the genre '{genre.get('Name')}'.")

                ses.send_email(
                    Source="songifytest@gmail.com",
                    Destination={"ToAddresses": [email]},
                    Message={
                        "Subject": {"Data": f"New artist in genre {genre.get('Name')}!"},
                        "Body": {
                            "Text": {
                                "Data": f"A new artist '{artist.get('Name')}' has been added to the genre '{genre.get('Name')}'."
                            }
                        }
                    }
                )

            print(
                f"[INFO] Sent notifications for artist '{artist.get('Name')}' "
                f"to {len(subscribers)} subscribers of genre '{genre.get('Name')}'"
            )

    except Exception as e:
        print(f"[ERROR] {e}")
        return {"statusCode": 500, "body": str(e)}

    return {"statusCode": 200, "body": "Processed message"}
