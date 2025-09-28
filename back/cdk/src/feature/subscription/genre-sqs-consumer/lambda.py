import os
import json
import boto3

sfn_client = boto3.client("stepfunctions")
STEP_FUNCTION_ARN = os.environ["STEP_FUNCTION_ARN"]

def lambda_handler(event, context):
    for record in event.get("Records", []):
        print(record)
        body = json.loads(record["body"])
        try:
            response = sfn_client.start_execution(
                stateMachineArn=STEP_FUNCTION_ARN,
                input=json.dumps(body)
            )
            print(f"[INFO] Started Step Function execution: {response['executionArn']} for message: {body}")
        except Exception as e:
            print(f"[ERROR] Could not start Step Function for message: {body}, error: {str(e)}")

    return {
        "statusCode": 200,
        "body": f"Processed {len(event.get('Records', []))} messages."
    }
