import os

from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_stepfunctions_tasks as tasks,
    aws_stepfunctions as sfn,
    Duration,
)
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_lambda import Function, StartingPosition, Runtime, Code
from aws_cdk.aws_lambda_event_sources import DynamoEventSource
from aws_cdk.aws_s3 import IBucket
from constructs import Construct


class AudioTranscriptionStack(Stack):
    def __init__(self, scope: Construct, id: str, *, table: ITable, songs_bucket: IBucket, **kwargs):
        super().__init__(scope, id, **kwargs)

        start_transcription_task = tasks.CallAwsService(
            self,
            "StartTranscription",
            service="transcribe",
            action="startTranscriptionJob",
            parameters={
                "TranscriptionJobName.$": "$.jobName",
                "MediaFormat.$": "$.mediaFormat",
                "Media": {
                    "MediaFileUri.$": "$.mediaFileUri"
                }
            },
            iam_resources=["*"],
            iam_action="transcribe:StartTranscriptionJob"
        )

        wait_task = sfn.Wait(
            self,
            "WaitForTranscription",
            time=sfn.WaitTime.duration(Duration.seconds(30))
        )

        check_status_task = tasks.CallAwsService(
            self,
            "GetTranscriptionJob",
            service="transcribe",
            action="getTranscriptionJob",
            parameters={
                "TranscriptionJobName.$": "$.jobName",
            },
            iam_resources=["*"],
            iam_action="transcribe:GetTranscriptionJob",
            output_path="$.TranscriptionJob"
        )

        transcription_consumer_lambda = Function(
            self,
            "AudioTranscriptionConsumerLambda",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/audio-transcription/consumer")),
            environment={
                "DYNAMO": table.table_name,
            }
        )

        transcription_consumer_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=["arn:aws:s3:::*"],
            )
        )
        table.grant_write_data(transcription_consumer_lambda)

        consume_result_task = tasks.LambdaInvoke(
            self,
            "AudioTranscriptionConsumeResult",
            lambda_function=transcription_consumer_lambda,
            payload=sfn.TaskInput.from_object(
                {
                    "jobName.$": '$.TranscriptionJobName',
                    "TranscriptFileUri.$": "$.Transcript.TranscriptFileUri"
                }
            ),
            output_path="$.Payload"
        )

        success_choice = sfn.Choice(self, "JobSucceeded?")
        definition = (
            start_transcription_task
            .next(wait_task)
            .next(check_status_task)
            .next(success_choice
                  .when(
                sfn.Condition.string_equals("$.TranscriptionJobStatus", "COMPLETED"),
                consume_result_task.next(sfn.Succeed(self, "Success"))
            )
                  .when(
                sfn.Condition.string_equals("$.TranscriptionJobStatus", "FAILED"),
                sfn.Fail(self, "Fail", cause="Transcription failed")
            )
                  .otherwise(wait_task)
                  )
        )

        transcription_state_machine = sfn.StateMachine(
            self, "TranscriptionStateMachine",
            definition=definition,
            timeout=Duration.minutes(10)
        )

        transcription_trigger_lambda = Function(
            self,
            "AudioTranscriptionTriggerLambda",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/audio-transcription/producer")),
            environment={
                "DYNAMO": table.table_name,
                "STATE_MACHINE_ARN": transcription_state_machine.state_machine_arn,
                "BUCKET_NAME" : songs_bucket.bucket_name
            }
        )

        transcription_state_machine.grant_start_execution(transcription_trigger_lambda)
        table.grant_stream_read(transcription_trigger_lambda)

        transcription_trigger_lambda.add_event_source(
            DynamoEventSource(
                table,
                starting_position=StartingPosition.LATEST,
                batch_size=5,
            )
        )
