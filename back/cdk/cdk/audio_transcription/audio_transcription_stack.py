from aws_cdk import (
    Stack, Fn, Duration,
)
from aws_cdk.aws_ecr import Repository
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode, Function, Code, Runtime
from aws_cdk.aws_s3 import EventType, NotificationKeyFilter, Bucket
from aws_cdk.aws_s3_notifications import LambdaDestination
from aws_cdk import aws_stepfunctions_tasks as tasks
import aws_cdk.aws_stepfunctions as sfn
from constructs import Construct


class AudioTranscriptionStack(Stack):
    def __init__(self, scope: Construct, id: str, *, region: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        songs_bucket = Bucket.from_bucket_arn(self, "ImportedBucket", bucket_arn=Fn.import_value("SongsBucketArn"))
        ecr_repo = Repository.from_repository_name(self, "AudioTranscribeRepo", repository_name="audio-transcribe")
        self.consumer_lambda = DockerImageFunction(
            self,
            "TranscriptionConsumerLambda",
            code=DockerImageCode.from_image_asset("src/feature/audio-transcription/consumer/container"),
            memory_size=2048,
            timeout=Duration.minutes(10),
            environment={
                "BUCKET_NAME": songs_bucket.bucket_name,
                "REGION": region,
                "MODEL_TYPE": "small"
            },
        )
        songs_bucket.grant_read_write(self.consumer_lambda)
        #
        # self.consumer_lambda.add_to_role_policy(PolicyStatement(
        #     effect=Effect.ALLOW,
        #     actions=["transcribe:StartTranscriptionJob"],
        #     resources=["*"]
        # ))

        start_transcription_task = tasks.LambdaInvoke(
            self,
            "RunTranscriptionTask",
            lambda_function=self.consumer_lambda,
            output_path="$.Payload"
        )
        start_transcription_task.add_retry(
            errors=["States.Timeout"],
            interval=Duration.minutes(2),
            max_attempts=3,
            backoff_rate=2.0
        )

        failed_state = sfn.Fail(self, "Failed")
        success_state = sfn.Succeed(self, "Success")

        definition = start_transcription_task.add_catch(failed_state).next(success_state)
        state_machine = sfn.StateMachine(
            self,
            "TranscriptionStateMachine",
            definition=definition,
            timeout=Duration.minutes(30)
        )

        self.producer_lambda = Function(
            self,
            "TranscriptionProducerLambda",
            handler="lambda.lambda_handler",
            code=Code.from_asset('src/feature/audio-transcription/producer'),
            environment={
                "STATE_MACHINE_ARN": state_machine.state_machine_arn,
            },
            timeout=Duration.seconds(30),
            runtime=Runtime.PYTHON_3_12
        )
        songs_bucket.grant_read_write(self.producer_lambda)
        state_machine.grant_start_execution(self.producer_lambda)
        songs_bucket.add_event_notification(
            EventType.OBJECT_CREATED,
            LambdaDestination(self.producer_lambda),
            NotificationKeyFilter(suffix=".mpeg")
        )