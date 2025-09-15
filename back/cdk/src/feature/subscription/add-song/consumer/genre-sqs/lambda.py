import json
import os
import boto3
from boto3.dynamodb.conditions import Key


sqs = boto3.client('sqs')
dynamodb = boto3.resource('dynamodb')
REGION = os.environ['REGION']
ses = boto3.client('ses', region_name=REGION)

SUBSCRIPTION_TABLE = os.environ["SUBSCRIPTION_TABLE"]

def lambda_handler(event, context):
    for record in event['Records']:
        try:
            message = json.loads(record['body'])
            msg_type = message.get('type')

            if msg_type != "SONG":
                continue

            song = message['song']
            genre = message.get('genre')
            if not genre:
                continue

            genre_id = genre.get('Id')

            table = dynamodb.Table(SUBSCRIPTION_TABLE)
            response = table.query(
                KeyConditionExpression = Key('PK').eq(f'GENRE#{genre_id}')
            )

            subscribers = response.get('Items', [])

            for sub in subscribers:
                email = sub.get('Email')
                if not email:
                    continue

                ses.send_email(
                    Source="songifytest@gmail.com",
                    Destination={"ToAddresses": [email]},
                    Message={
                        "Subject": {"Data": f"New song in genre {genre.get('Name')}!"},
                        "Body": {
                            "Text": {"Data": f"A new song '{song.get('Name')}' has been added to the genre '{genre.get('Name')}'."}
                        }
                    }
                )

            print(f"[INFO] Sent notifications for song {song.get('Name')} to {len(subscribers)} subscribers of genre {genre.get('Name')}")

        except Exception as e:
            print(f"[ERROR] {e}")
            continue

    return {"statusCode": 200, "body": "Processed messages"}
