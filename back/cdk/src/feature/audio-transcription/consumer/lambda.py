import os
import uuid
from urllib.parse import unquote_plus

import boto3

transcribe_client = boto3.client('transcribe')

def lambda_handler(event, _context):
    for record in event["Records"]:
        s3_info = record["s3"]
        bucket = s3_info["bucket"]["name"]
        key = unquote_plus(s3_info["object"]["key"])
        song_id = key.split("/")[0]
        ext = os.path.splitext(key)[1].lower()

        job_name = f"transcription-song-{song_id}-{str(uuid.uuid4())}"
        media_uri = f"s3://{bucket}/{key}"

        try:
            response = transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={"MediaFileUri": media_uri},
                MediaFormat="mp3",
                IdentifyLanguage=True,
                OutputBucketName = bucket,
                OutputKey=f'{song_id}/transcription/transcription.json'
            )
        except Exception as e:
            print(e)

