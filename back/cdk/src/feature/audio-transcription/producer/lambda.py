import json

import boto3
import os

TABLE_NAME = os.environ['DYNAMO']
table = boto3.resource('dynamodb').Table(TABLE_NAME)
STATE_MACHINE_ARN = os.environ['STATE_MACHINE_ARN']
stepfunctions_client = boto3.client('stepfunctions')
BUCKET_NAME = os.environ['BUCKET_NAME']


def lambda_handler(event, context):
    for record in event["Records"]:
        if record["eventName"] != "INSERT":
            continue
        try:
            new_item = record["dynamodb"]["NewImage"]
            pk = new_item["PK"]["S"]
            if not pk.startswith("SONG#"):
                continue
            audio_path:str = new_item["AudioPath"]["S"]
            job_name = pk.replace("SONG#", "transcription-job-")
            full_uri = f"s3://{BUCKET_NAME}/{audio_path}"
            input_data = {
                "jobName": job_name,
                "mediaFormat" : audio_path.split(".")[-1],
                "mediaFileUri": full_uri
            }
            print("here")
            print(input_data)
            response = stepfunctions_client.start_execution(
                stateMachineArn=STATE_MACHINE_ARN,
                input=json.dumps(input_data)
            )
        except Exception as ex:
            print("Exception")
            print(ex)
            continue