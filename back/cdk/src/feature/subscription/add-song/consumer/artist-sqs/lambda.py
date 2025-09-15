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

            song = message.get('song')
            artist = message.get('artist')
            if not artist or not song:
                continue

            artist_id = artist.get('Id')
            artist_name = artist.get('Name')

            table = dynamodb.Table(SUBSCRIPTION_TABLE)
            response = table.query(
                KeyConditionExpression=Key('PK').eq(f'ARTIST#{artist_id}')
            )
            subscribers = response.get('Items', [])

            for sub in subscribers:
                email = sub.get('Email')
                if not email:
                    continue

                ses.send_email(
                    Source="songifytest@gmail.com",  # mora biti verifikovan
                    Destination={"ToAddresses": [email]},
                    Message={
                        "Subject": {"Data": f"New song from {artist_name}!"},
                        "Body": {
                            "Text": {
                                "Data": f"A new song '{song.get('Name')}' has been released by '{artist_name}'."
                            }
                        }
                    }
                )

            print(f"[INFO] Sent notifications for song '{song.get('Name')}' to {len(subscribers)} subscribers of artist '{artist_name}'")

        except Exception as e:
            print(f"[ERROR] {e}")
            continue

    return {"statusCode": 200, "body": "Processed messages"}
