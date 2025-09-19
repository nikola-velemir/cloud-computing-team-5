import os
import time
import uuid
from urllib.parse import unquote_plus
import boto3
import requests

s3 = boto3.client("s3")
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OUTPUT_BUCKET = os.environ["BUCKET_NAME"]
MAX_RETRIES=5

def call_whisper(file_path):
    for attempt in range(1, MAX_RETRIES + 1):
        with open(file_path, "rb") as f:
            try:
                response = requests.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                    files={"file": f},
                    data={"model": "whisper-1"},
                    timeout=300
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    wait = 2 ** attempt
                    print(f"Rate limit hit. Retry in {wait}s...")
                    time.sleep(wait)
                else:
                    raise
    raise Exception("Max retries exceeded for Whisper API")

def lambda_handler(event, context):
    for record in event["Records"]:
        s3_info = record["s3"]
        bucket = s3_info["bucket"]["name"]
        key = unquote_plus(s3_info["object"]["key"])
        song_id = key.split("/")[0]
        ext = os.path.splitext(key)[1].lower()

        download_path = f"/tmp/{uuid.uuid4()}{ext}"
        s3.download_file(bucket, key, download_path)

        try:
            transcript_response = call_whisper(download_path)
        except Exception as e:
            print(f"Whisper API error for {key}: {e}")
            continue

        transcript_text = transcript_response.get("text", "")
        output_key = f"{song_id}/lyrics/lyrics.txt"

        s3.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=output_key,
            Body=transcript_text.encode("utf-8")
        )
        print(f"Transcript saved to s3://{OUTPUT_BUCKET}/{output_key}")
# def lambda_handler(event, _context):
#     for record in event["Records"]:
#         s3_info = record["s3"]
#         bucket = s3_info["bucket"]["name"]
#         key = unquote_plus(s3_info["object"]["key"])
#         song_id = key.split("/")[0]
#         ext = os.path.splitext(key)[1].lower()
#
#         job_name = f"transcription-song-{song_id}-{str(uuid.uuid4())}"
#         media_uri = f"s3://{bucket}/{key}"
#
#         try:
#             response = transcribe_client.start_transcription_job(
#                 TranscriptionJobName=job_name,
#                 Media={"MediaFileUri": media_uri},
#                 MediaFormat='mp3',
#                 IdentifyLanguage=True,
#                 OutputBucketName = bucket,
#                 MediaSampleRateHertz = 16000,
#                 OutputKey=f'{song_id}/lyrics/lyrics.json',
#             )
#             print(response)
#         except Exception as e:
#             print(e)

