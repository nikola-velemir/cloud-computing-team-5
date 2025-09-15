import os

from aws_cdk import Stack
from aws_cdk.aws_apigateway import LambdaIntegration, IRestApi
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_lambda import Function, Runtime, Code, LayerVersion, StartingPosition
from aws_cdk.aws_lambda_event_sources import DynamoEventSource
from aws_cdk.aws_s3 import IBucket
from aws_cdk.aws_sqs import IQueue
from constructs import Construct

from cdk.cors_helper import add_cors_options


class SubscriptionStack(Stack):
    def __init__(self, scope: Construct, id: str, api: IRestApi, dynamoDb: ITable, subscriptionDynamoDb: ITable, albums_bucket: IBucket, genre_bucket:IBucket,
                 artists_bucket: IBucket, song_bucket: IBucket,genre_sqs: IQueue,album_sqs: IQueue,artist_sqs: IQueue, **kwargs):
        super().__init__(scope, id, **kwargs)

        subscription_api = api.root.add_resource("subscription")

        dynamo_add_song_lambda = Function(
            self,
            "DynamoAddSong",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(
                os.path.join(os.getcwd(), "src/feature/subscription/add-song/producer"),
            ),
            environment={
                "ALBUM_QUEUE_URL": album_sqs.queue_url,
                "ARTIST_QUEUE_URL": artist_sqs.queue_url,
                "GENRE_QUEUE_URL": genre_sqs.queue_url,
            },
        )

        album_sqs.grant_send_messages(dynamo_add_song_lambda)
        artist_sqs.grant_send_messages(dynamo_add_song_lambda)
        genre_sqs.grant_send_messages(dynamo_add_song_lambda)

        dynamo_add_song_lambda.add_event_source(
            DynamoEventSource(
                dynamoDb,
                starting_position=StartingPosition.LATEST,
                batch_size=5
            )
        )
