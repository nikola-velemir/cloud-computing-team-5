import os

from aws_cdk import (
    Stack,
)
from aws_cdk.aws_s3_notifications import LambdaDestination
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_iam import PolicyStatement, Effect
from aws_cdk.aws_lambda import Function, Code, Runtime, StartingPosition
from aws_cdk.aws_lambda_event_sources import DynamoEventSource, S3EventSource
from aws_cdk.aws_s3 import IBucket, EventType, NotificationKeyFilter
from constructs import Construct


class AudioTranscriptionStack(Stack):
    def __init__(self, scope: Construct, id: str, *, table: ITable, songs_bucket: IBucket, region: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        #
        # self.trigger_lambda = Function(
        #     self,
        #     "TranscriptionTriggerLambda",
        #     code=Code.from_asset('src/feature/audio-transcription/consumer'),
        #     runtime=Runtime.PYTHON_3_11,
        #     handler="lambda.lambda_handler",
        #     environment={
        #         "BUCKET_NAME": songs_bucket.bucket_name,
        #         "REGION": region,
        #     },
        # )
        # table.grant_read_write_data(self.trigger_lambda )
        # songs_bucket.grant_read_write(self.trigger_lambda )
        #
        # self.trigger_lambda.add_to_role_policy(PolicyStatement(
        #     effect=Effect.ALLOW,
        #     actions=["transcribe:StartTranscriptionJob"],
        #     resources=["*"]
        # ))
