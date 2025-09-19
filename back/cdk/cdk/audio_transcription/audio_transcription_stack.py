import os

from aws_cdk import (
    Stack, Fn, Duration
)
from aws_cdk.aws_s3_notifications import LambdaDestination
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_iam import PolicyStatement, Effect
from aws_cdk.aws_lambda import Function, Code, Runtime, StartingPosition
from aws_cdk.aws_lambda_event_sources import DynamoEventSource, S3EventSource
from aws_cdk.aws_s3 import IBucket, EventType, NotificationKeyFilter, Bucket
from constructs import Construct
from aws_cdk import aws_lambda as _lambda


class AudioTranscriptionStack(Stack):
    def __init__(self, scope: Construct, id: str, *,region: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.openai_layer = _lambda.LayerVersion(
            self, "OpenaiLayer",
            code=_lambda.Code.from_asset("layers/transcription-layer"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9, _lambda.Runtime.PYTHON_3_10, _lambda.Runtime.PYTHON_3_11],
            description="Lambda OpenAI layer"
        )

        songs_bucket = Bucket.from_bucket_arn(self, "ImportedBucket", bucket_arn=Fn.import_value("SongsBucketArn"))
        self.trigger_lambda = Function(
            self,
            "TranscriptionTriggerLambda",
            code=Code.from_asset('src/feature/audio-transcription/consumer'),
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            environment={
                "OPENAI_API_KEY": "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",
                "BUCKET_NAME": songs_bucket.bucket_name,
                "REGION": region,
            },
            layers=[self.openai_layer]
        )
        songs_bucket.grant_read_write(self.trigger_lambda)

        self.trigger_lambda.add_to_role_policy(PolicyStatement(
            effect=Effect.ALLOW,
            actions=["transcribe:StartTranscriptionJob"],
            resources=["*"]
        ))
        songs_bucket.add_event_notification(
            EventType.OBJECT_CREATED,
            LambdaDestination(self.trigger_lambda),
            NotificationKeyFilter(suffix=".mpeg")
        )

