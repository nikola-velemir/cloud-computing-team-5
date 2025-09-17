import os

from aws_cdk import Stack, Duration
from aws_cdk.aws_apigateway import LambdaIntegration, IRestApi
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_lambda import Function, Runtime, Code, LayerVersion, StartingPosition
from aws_cdk.aws_lambda_event_sources import DynamoEventSource, SqsEventSource
from aws_cdk.aws_s3 import IBucket
from aws_cdk.aws_sqs import IQueue
from constructs import Construct
from aws_cdk import aws_iam as iam
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_stepfunctions_tasks as tasks
from aws_cdk import aws_stepfunctions as sfn



from cdk.cors_helper import add_cors_options


class FeedStack(Stack):
    def __init__(self, scope: Construct, id: str, api: IRestApi, dynamoDb: ITable, subscriptionDynamoDb: ITable,
                 reviewDynamoDb: ITable, feedDynamoDb: ITable,
                 utils_layer: LayerVersion,feed_sqs: IQueue
                 ,region: str,authorizer: apigw.CognitoUserPoolsAuthorizer, **kwargs):


        super().__init__(scope, id, **kwargs)

        feed_api = api.root.add_resource("feed")

        #   SUBSCRIPTION
        subscribe_producer = Function(
            self, "SubscribeFeedProducer",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/feed/subscribe/producer"),
            environment={
                "FEED_SQS_URL": feed_sqs.queue_url,
            }
        )
        feed_sqs.grant_send_messages(subscribe_producer)
        subscribe_producer.add_event_source(
            DynamoEventSource(
                subscriptionDynamoDb,
                starting_position=StartingPosition.LATEST,
                batch_size=5
            )
        )


        subscribe_consumer = Function(
            self, "SubscribeFeedConsumer",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/feed/subscribe/consumer"),
            environment={
                "FEED_TABLE": feedDynamoDb.table_name,
            }
        )
        feedDynamoDb.grant_read_data(subscribe_consumer)
        feedDynamoDb.grant_write_data(subscribe_consumer)
        # feed_sqs.grant_consume_messages(subscribe_consumer)
        # subscribe_consumer.add_event_source(SqsEventSource(
        #         feed_sqs,
        #         batch_size=5
        #     ))

        #   REVIEW
        review_producer = Function(
            self, "ReviewFeedProducer",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/feed/review/producer"),
            environment={
                "FEED_SQS_URL": feed_sqs.queue_url,
            }
        )
        feed_sqs.grant_send_messages(review_producer)
        review_producer.add_event_source(
            DynamoEventSource(
                reviewDynamoDb,
                starting_position=StartingPosition.LATEST,
                batch_size=5
            )
        )

        review_consumer = Function(
            self, "ReviewFeedConsumer",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/feed/review/consumer"),
            environment={
                "FEED_TABLE": feedDynamoDb.table_name,
            }
        )
        feedDynamoDb.grant_read_data(review_consumer)
        feedDynamoDb.grant_write_data(review_consumer)


        #   PLAY_SONG
        song_consumer = Function(
            self, "SongFeedConsumer",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/feed/play-song/consumer"),
            environment={
                "FEED_TABLE": feedDynamoDb.table_name,
            }
        )
        feedDynamoDb.grant_read_data(song_consumer)
        feedDynamoDb.grant_write_data(song_consumer)

        #   PLAY_ALBUM
        album_consumer = Function(
            self, "AlbumFeedConsumer",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/feed/play-album/consumer"),
            environment={
                "FEED_TABLE": feedDynamoDb.table_name,
            }
        )
        feedDynamoDb.grant_read_data(album_consumer)
        feedDynamoDb.grant_write_data(album_consumer)