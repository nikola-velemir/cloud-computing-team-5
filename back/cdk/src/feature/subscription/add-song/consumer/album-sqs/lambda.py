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
        album = event.get('album')
        if not album or not song:
            return {"statusCode": 400, "body": "Missing song or album"}

        album_id = album.get('Id')
        album_name = album.get('Title')

        table = dynamodb.Table(SUBSCRIPTION_TABLE)
        response = table.query(
            KeyConditionExpression=Key('PK').eq(f'ALBUM#{album_id}')
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
                    "Subject": {"Data": f"New song in album {album_name}!"},
                    "Body": {
                        "Text": {
                            "Data": f"A new song '{song.get('Name')}' has been added to the album '{album_name}'."
                        }
                    }
                }
            )

        print(f"[INFO] Sent notifications for song '{song.get('Name')}' to {len(subscribers)} subscribers of album '{album_name}'")

    except Exception as e:
        print(f"[ERROR] {e}")
        return {"statusCode": 500, "body": str(e)}

    return {"statusCode": 200, "body": "Processed message"}
