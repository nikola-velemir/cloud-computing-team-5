import json
import os
import uuid
from operator import contains
from urllib.request import urlopen

import boto3

transcribe_client = boto3.client('transcribe')
BUCKET_NAME = os.environ["BUCKET_NAME"]

def lambda_handler(event, _context):
    for record in event["Records"]:
        print(record)
        if record["eventName"] != "INSERT":
            continue
        try:
            new_item = record["dynamodb"]["NewImage"]
            pk: str = new_item["PK"]["S"]
            if not "SONG#" in pk:
                continue
            cover_path:str = new_item["CoverPath"]["S"]
            lyrics_path:str = new_item["Lyrics"]["S"]
            song_id = pk.split("#")[-1]
            full_uri = f's3://{BUCKET_NAME}/{cover_path}'
            format = cover_path.split(".")[-1]
            job_name = f'transcription-job-{song_id}-{uuid.uuid4()}'

            response = transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': full_uri},
                MediaFormat=format,
                OutputBucketName=BUCKET_NAME,
                OutputKey=lyrics_path
            )
        except Exception as ex:
            print(ex)
            continue
