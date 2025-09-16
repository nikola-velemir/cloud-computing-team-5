import json
import os
from urllib.request import urlopen

import boto3

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ['DYNAMO']
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    job_name = event['jobName']
    transcript_uri = event['TranscriptFileUri']

    with urlopen(transcript_uri) as response:
        transcript_json = json.loads(response.read())

    transcript_text = transcript_json['results']['transcripts'][0]['transcript']

    song_id = job_name.replace("transcription-job-", "SONG#")

    # Update DynamoDB
    table.update_item(
        Key={'PK': song_id},
        UpdateExpression="SET lyrics.lyrics = :text",
        ExpressionAttributeValues={':text': transcript_text}
    )

    return {"status": "success", "songId": song_id, "transcriptLength": len(transcript_text)}