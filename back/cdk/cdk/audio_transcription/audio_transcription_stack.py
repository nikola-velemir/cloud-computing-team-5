import os

from aws_cdk import (
    Stack, Fn,
)
from aws_cdk.aws_s3_notifications import LambdaDestination
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_iam import PolicyStatement, Effect
from aws_cdk.aws_lambda import Function, Code, Runtime, StartingPosition, DockerImageFunction, DockerImageCode
from aws_cdk.aws_lambda_event_sources import DynamoEventSource, S3EventSource
from aws_cdk.aws_s3 import IBucket, EventType, NotificationKeyFilter, Bucket
from constructs import Construct


class AudioTranscriptionStack(Stack):
    def __init__(self, scope: Construct, id: str, *,region: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        songs_bucket = Bucket.from_bucket_arn(self, "ImportedBucket", bucket_arn=Fn.import_value("SongsBucketArn"))
        self.trigger_lambda = DockerImageFunction(
            self,
            "TranscriptionTriggerLambda",
            code=DockerImageCode.from_image_asset('src/feature/audio-transcription/consumer/container'),
            environment={
                "BUCKET_NAME": songs_bucket.bucket_name,
                "REGION": region,
            },
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