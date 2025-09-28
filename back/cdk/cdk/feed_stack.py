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
                 utils_layer: LayerVersion, feed_sqs: IQueue
                 ,region: str,authorizer: apigw.CognitoUserPoolsAuthorizer,
                 song_bucket: IBucket, artists_bucket: IBucket, albums_bucket: IBucket,
                 genre_bucket: IBucket,
                               **kwargs):


        super().__init__(scope, id, **kwargs)

        feed_api = api.root.add_resource("feed")

        # fetch items from feed by user
        fetch_feed = Function(
            self, "FetchFeed",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/feed/fetch-items"),
            environment={
                "FEED_TABLE": feedDynamoDb.table_name,
                "SONG_BUCKET": song_bucket.bucket_name,
                "ARTIST_BUCKET": artists_bucket.bucket_name,
                "GENRE_BUCKET": genre_bucket.bucket_name,
                "ALBUM_BUCKET": albums_bucket.bucket_name,
                "EXPIRATION_TIME": "1800",
                "REGION": region
            },
            layers=[utils_layer],
        )
        feedDynamoDb.grant_read_data(fetch_feed)
        song_bucket.grant_read(fetch_feed)
        artists_bucket.grant_read(fetch_feed)
        albums_bucket.grant_read(fetch_feed)
        genre_bucket.grant_read(fetch_feed)
        feed_api.add_method(
            "GET",
            LambdaIntegration(fetch_feed, proxy=True),
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=authorizer,
        )
        feed_api.add_method(
            "OPTIONS",
            apigw.MockIntegration(
                integration_responses=[apigw.IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Headers":
                            "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                        "method.response.header.Access-Control-Allow-Origin": "'*'",
                        "method.response.header.Access-Control-Allow-Methods":
                            "'GET,OPTIONS'",
                    },
                )],
                passthrough_behavior=apigw.PassthroughBehavior.WHEN_NO_MATCH,
                request_templates={"application/json": '{"statusCode": 200}'},
            ),
            method_responses=[apigw.MethodResponse(
                status_code="200",
                response_parameters={
                    "method.response.header.Access-Control-Allow-Headers": True,
                    "method.response.header.Access-Control-Allow-Methods": True,
                    "method.response.header.Access-Control-Allow-Origin": True,
                },
            )]
        )

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

        # new entity
        new_entity_consumer = Function(
            self, "NewEntityConsumer",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/feed/new-entity"),
            environment={
                "FEED_TABLE": feedDynamoDb.table_name,
            }
        )
        feedDynamoDb.grant_read_data(new_entity_consumer)
        feedDynamoDb.grant_write_data(new_entity_consumer)

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


        #  STEP FUNCTION

        subscribe_consumer_task = tasks.LambdaInvoke(
            self, "ProcessSubscribe",
            lambda_function=subscribe_consumer,
            output_path="$.Payload"
        )

        review_consumer_task = tasks.LambdaInvoke(
            self, "ProcessReview",
            lambda_function=review_consumer,
            output_path="$.Payload"
        )

        new_entity_consumer_task = tasks.LambdaInvoke(
            self, "ProcessNewEntity",
            lambda_function=new_entity_consumer,
            output_path="$.Payload"
        )

        song_consumer_task = tasks.LambdaInvoke(
            self, "ProcessSong",
            lambda_function=song_consumer,
            output_path="$.Payload"
        )

        album_consumer_task = tasks.LambdaInvoke(
            self, "ProcessAlbum",
            lambda_function=album_consumer,
            output_path="$.Payload"
        )

        choice_feed = sfn.Choice(self, "CheckFeedType")
        definition_feed = (
            choice_feed
            .when(sfn.Condition.string_equals("$.type", "REVIEW"), review_consumer_task)
            .when(sfn.Condition.string_equals("$.type", "SUBSCRIBE"), subscribe_consumer_task)
            .when(sfn.Condition.string_equals("$.type", "PLAY_SONG"), song_consumer_task)
            .when(sfn.Condition.string_equals("$.type", "PLAY_ALBUM"), album_consumer_task)
            .when(sfn.Condition.string_equals("$.type", "NEW_ENTITY"), new_entity_consumer_task)
            .otherwise(sfn.Fail(self, "UnknownTypeForGenreStepFn",
                                cause="Unsupported event type",
                                error="TypeNotSupported"))
        )

        state_machine_feed = sfn.StateMachine(
            self, "FeedStateMachine",
            definition=definition_feed,
            timeout=Duration.minutes(5)
        )

        feed_sqs_consumer = Function(
            self, "FeedMainConsumer",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/feed/main-consumer"),
            environment={
                "STEP_FUNCTION_ARN": state_machine_feed.state_machine_arn
            }
        )
        state_machine_feed.grant_start_execution(feed_sqs_consumer)
        feed_sqs.grant_consume_messages(feed_sqs_consumer)
        feed_sqs_consumer.add_event_source(SqsEventSource(
            feed_sqs,
            batch_size=5
        ))