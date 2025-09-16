import os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
REGION = os.environ['REGION']
ses = boto3.client('ses', region_name=REGION)

SUBSCRIPTION_TABLE = os.environ["SUBSCRIPTION_TABLE"]

def lambda_handler(event, context):
    try:
        msg_type = event.get('type')
        if msg_type != "SONG":
            return {"statusCode": 400, "body": "Not a SONG event"}

        song = event.get('song')
        artist = event.get('artist')
        if not artist or not song:
            return {"statusCode": 400, "body": "Missing song or artist"}

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
                Source="songifytest@gmail.com",
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
        return {"statusCode": 500, "body": str(e)}

    return {"statusCode": 200, "body": "Processed message"}
