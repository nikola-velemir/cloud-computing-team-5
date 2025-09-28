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
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_lambda as _lambda



from cdk.cors_helper import add_cors_options


class SubscriptionStack(Stack):
    def __init__(self, scope: Construct, id: str, api: IRestApi, dynamoDb: ITable, subscriptionDynamoDb: ITable,
                 utils_layer: LayerVersion,genre_sqs: IQueue,album_sqs: IQueue,artist_sqs: IQueue,region: str,
                 authorizer: apigw.CognitoUserPoolsAuthorizer, feed_sqs: IQueue, **kwargs):
        super().__init__(scope, id, **kwargs)

        subscription_api = api.root.add_resource("subscription")


        # trigger when new song was added
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
            }

        )
        album_sqs.grant_send_messages(dynamo_add_song_lambda)
        artist_sqs.grant_send_messages(dynamo_add_song_lambda)
        genre_sqs.grant_send_messages(dynamo_add_song_lambda)

        #trigger when new album was created
        dynamo_add_album_lambda = Function(
            self,
            "DynamoTriggerAddAlbum",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(
                os.path.join(os.getcwd(), "src/feature/subscription/add-album/producer"),
            ),
            environment={
                "ARTIST_QUEUE_URL": artist_sqs.queue_url,
                "GENRE_QUEUE_URL": genre_sqs.queue_url,
            },
        )
        album_sqs.grant_send_messages(dynamo_add_album_lambda)
        artist_sqs.grant_send_messages(dynamo_add_album_lambda)
        genre_sqs.grant_send_messages(dynamo_add_album_lambda)

        # trigger when new artist was created
        dynamo_add_artist_lambda = Function(
            self,
            "DynamoTriggerAddArtist",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(
                os.path.join(os.getcwd(), "src/feature/subscription/add-artist/producer"),
            ),
            environment={
                "GENRE_QUEUE_URL": genre_sqs.queue_url,
            },
        )
        album_sqs.grant_send_messages(dynamo_add_artist_lambda)
        artist_sqs.grant_send_messages(dynamo_add_artist_lambda)
        genre_sqs.grant_send_messages(dynamo_add_artist_lambda)

        artist_task = tasks.LambdaInvoke(
            self, "ProcessArtist",
            lambda_function=dynamo_add_artist_lambda,
            output_path="$.Payload"
        )

        album_task = tasks.LambdaInvoke(
            self, "ProcessAlbum",
            lambda_function=dynamo_add_album_lambda,
            output_path="$.Payload"
        )

        song_task = tasks.LambdaInvoke(
            self, "ProcessSong",
            lambda_function=dynamo_add_song_lambda,
            output_path="$.Payload"
        )

        choice = sfn.Choice(self, "CheckType")
        definition = (
            choice
            .when(sfn.Condition.string_equals("$.type", "ARTIST"), artist_task)
            .when(sfn.Condition.string_equals("$.type", "ALBUM"), album_task)
            .when(sfn.Condition.string_equals("$.type", "SONG"), song_task)
            .otherwise(sfn.Fail(self, "UnknownType",
                                cause="Unsupported event type",
                                error="TypeNotSupported"))
        )

        state_machine = sfn.StateMachine(
            self, "SubscriptionStateMachine",
            definition=definition,
            timeout=Duration.minutes(5)
        )

        dynamo_stream_to_sfn = Function(
            self, "DynamoStreamToStepFn",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/subscription/step-producer"),
            environment={
                "STEP_FUNCTION_ARN": state_machine.state_machine_arn
            }
        )
        state_machine.grant_start_execution(dynamo_stream_to_sfn)
        dynamo_stream_to_sfn.add_event_source(
            DynamoEventSource(
                dynamoDb,
                starting_position=StartingPosition.LATEST,
                batch_size=5
            )
        )

        consumer_add_artist_to_genre = Function(
            self,
            "ConsumerAddArtistToGenre",
            handler="lambda.lambda_handler",
            runtime=Runtime.PYTHON_3_11,
            code=Code.from_asset(
                os.path.join(os.getcwd(), "src/feature/subscription/add-artist/consumer/genre-sqs")),
            environment={
                "SUBSCRIPTION_TABLE": subscriptionDynamoDb.table_name,
                "REGION": region,
                "FEED_SQS_URL": feed_sqs.queue_url
            }


        )
        feed_sqs.grant_send_messages(consumer_add_artist_to_genre)
        consumer_add_artist_to_genre.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ses:SendEmail", "ses:SendRawEmail"],
                resources=["*"]
            )
        )
        subscriptionDynamoDb.grant_read_write_data(consumer_add_artist_to_genre)
        # consumer_add_artist_to_genre.add_event_source(SqsEventSource(genre_sqs))


        # trigger when something-SONG was added to genre_sqs
        consumer_add_song_to_genre = Function(
            self,
            "ConsumerAddSongToGenre",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(
                os.path.join(os.getcwd(), "src/feature/subscription/add-song/consumer/genre-sqs")),
            environment={
                "SUBSCRIPTION_TABLE": subscriptionDynamoDb.table_name,
                "REGION": region,
                "FEED_SQS_URL": feed_sqs.queue_url
            }
        )
        feed_sqs.grant_send_messages(consumer_add_song_to_genre)
        consumer_add_song_to_genre.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ses:SendEmail", "ses:SendRawEmail"],
                resources=["*"]
            )
        )
        subscriptionDynamoDb.grant_read_write_data(consumer_add_song_to_genre)
        # consumer_add_song_to_genre.add_event_source(SqsEventSource(genre_sqs))

        # trigger when something-SONG was added to album
        consumer_add_song_to_album = Function(
            self,
            "ConsumerAddSongToAlbum",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(
                os.path.join(os.getcwd(), "src/feature/subscription/add-song/consumer/album-sqs")),
            environment={
                "SUBSCRIPTION_TABLE": subscriptionDynamoDb.table_name,
                "REGION": region,
                "FEED_SQS_URL": feed_sqs.queue_url
            }
        )
        feed_sqs.grant_send_messages(consumer_add_song_to_album)
        consumer_add_song_to_album.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ses:SendEmail", "ses:SendRawEmail"],
                resources=["*"]
            )
        )
        subscriptionDynamoDb.grant_read_write_data(consumer_add_song_to_album)
        consumer_add_song_to_album.add_event_source(SqsEventSource(album_sqs))

        # trigger when something-SONG was added to artist_sqs
        consumer_add_song_to_artist = Function(
            self,
            "ConsumerAddSongToArtist",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(
                os.path.join(os.getcwd(), "src/feature/subscription/add-song/consumer/artist-sqs")),
            environment={
                "SUBSCRIPTION_TABLE": subscriptionDynamoDb.table_name,
                "REGION": region,
                "FEED_SQS_URL": feed_sqs.queue_url
            }
        )
        feed_sqs.grant_send_messages(consumer_add_song_to_artist)
        consumer_add_song_to_artist.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ses:SendEmail", "ses:SendRawEmail"],
                resources=["*"]
            )
        )
        subscriptionDynamoDb.grant_read_write_data(consumer_add_song_to_artist)
        # consumer_add_song_to_artist.add_event_source(SqsEventSource(artist_sqs))

        # trigger when album was added to artist-sqs
        consumer_add_album_to_artist = Function(
            self,
            "ConsumerAddAlbumToArtist",
            handler="lambda.lambda_handler",
            runtime=Runtime.PYTHON_3_11,
            code=Code.from_asset(
                os.path.join(os.getcwd(), "src/feature/subscription/add-album/consumer/artist-sqs")),
            environment={
                "SUBSCRIPTION_TABLE": subscriptionDynamoDb.table_name,
                "REGION": region,
                "FEED_SQS_URL": feed_sqs.queue_url
            }
        )
        consumer_add_album_to_artist.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ses:SendEmail", "ses:SendRawEmail"],
                resources=["*"]
            )
        )
        feed_sqs.grant_send_messages(consumer_add_album_to_artist)
        subscriptionDynamoDb.grant_read_write_data(consumer_add_album_to_artist)
        # consumer_add_album_to_artist.add_event_source(SqsEventSource(artist_sqs))

        # trigger when album was added  to genre-sqs
        consumer_add_album_to_genre = Function(
            self,
            "ConsumerAddAlbumToGenre",
            handler="lambda.lambda_handler",
            runtime=Runtime.PYTHON_3_11,
            code=Code.from_asset(
                os.path.join(os.getcwd(), "src/feature/subscription/add-album/consumer/genre-sqs")),
            environment={
                "SUBSCRIPTION_TABLE": subscriptionDynamoDb.table_name,
                "REGION": region,
                "FEED_SQS_URL": feed_sqs.queue_url
            }

        )
        feed_sqs.grant_send_messages(consumer_add_album_to_genre)
        consumer_add_album_to_genre.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ses:SendEmail", "ses:SendRawEmail"],
                resources=["*"]
            )
        )
        subscriptionDynamoDb.grant_read_write_data(consumer_add_album_to_genre)
        # consumer_add_album_to_genre.add_event_source(SqsEventSource(genre_sqs))

        # subs
        subscribe_user_to_content = Function(
            self, "SubscribeUserToContent",
            runtime = Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code = Code.from_asset("src/feature/subscription/subscribe"),
            environment={
                "SUBSCRIPTION_TABLE": subscriptionDynamoDb.table_name,
            },
            layers=[utils_layer],
        )

        subscriptionDynamoDb.grant_read_data(subscribe_user_to_content)
        subscriptionDynamoDb.grant_write_data(subscribe_user_to_content)

        subscribe_api = subscription_api.add_resource("subscribe")
        subscribe_api.add_method(
            "POST",
            LambdaIntegration(subscribe_user_to_content, proxy=True),
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=authorizer,
        )


        # unsub
        user_unsubsrbie = Function(
            self,
            "UserUnsubscribe",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/subscription/unsubscribe"),
            environment={
                "SUBSCRIPTION_TABLE": subscriptionDynamoDb.table_name,
            },
            layers=[utils_layer],
        )
        subscriptionDynamoDb.grant_read_data(user_unsubsrbie)
        subscriptionDynamoDb.grant_write_data(user_unsubsrbie)
        subscriptionDynamoDb.grant_full_access(user_unsubsrbie)

        unsubscribe_api = subscription_api.add_resource("unsubscribe")
        unsubscribe_api.add_method(
            "DELETE",
            LambdaIntegration(user_unsubsrbie, proxy=True),
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=authorizer,
        )
        add_cors_options(unsubscribe_api)

        # GSI
        subscriptionDynamoDb.add_global_secondary_index(
            index_name="UserIndex",
            partition_key=dynamodb.Attribute(name="SK", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="PK", type=dynamodb.AttributeType.STRING),  # optional
            projection_type=dynamodb.ProjectionType.ALL
        )

        # get subs
        get_subscription_by_user = Function(
            self,
            "GetSubscriptionByUser",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/subscription/get-subscription-by-user"),
            environment={
                "SUBSCRIPTION_TABLE": subscriptionDynamoDb.table_name,
            },
            layers=[utils_layer],
        )
        subscriptionDynamoDb.grant_read_data(get_subscription_by_user)
        subscribe_api.add_method(
            "GET",
            LambdaIntegration(get_subscription_by_user, proxy=True),
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=authorizer,
        )
        add_cors_options(subscribe_api)

        # is sub
        is_user_subscribed = Function(
            self, "IsUserSubscribed",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/subscription/is-subscribed"),
            environment={
                "SUBSCRIPTION_TABLE": subscriptionDynamoDb.table_name,
            },
            layers=[utils_layer],
        )

        subscriptionDynamoDb.grant_read_data(is_user_subscribed)
        subscriptionDynamoDb.grant_write_data(is_user_subscribed)

        is_subscribe_api = subscription_api.add_resource("is-subscribed")
        is_subscribe_api.add_method(
            "GET",
            LambdaIntegration(is_user_subscribed, proxy=True),
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=authorizer,
        )
        add_cors_options(is_subscribe_api)

        consumer_add_artist_to_genre_task = tasks.LambdaInvoke(
            self, "ProcessArtistForGenre",
            lambda_function=consumer_add_artist_to_genre,
            output_path="$.Payload"
        )

        consumer_add_album_to_genre_task = tasks.LambdaInvoke(
            self, "ProcessAlbumForGenre",
            lambda_function=consumer_add_album_to_genre,
            output_path="$.Payload"
        )

        consumer_add_song_to_genre_task = tasks.LambdaInvoke(
            self, "ProcessSongForGenre",
            lambda_function=consumer_add_song_to_genre,
            output_path="$.Payload"
        )


        # album_sqs na njega se kaci samo consumer_add_song_to_album
        # genre_sqs na njega se kaci consumer_add_artist_to_genre_task, consumer_add_album_to_genre_task, consumer_add_song_to_genre_task
        # artist_sqs na njega se kaci consumer_add_album_to_artist_task, consumer_add_song_to_artist_task
        choice_genre = sfn.Choice(self, "CheckGenreType")
        definition_genre = (
            choice_genre
            .when(sfn.Condition.string_equals("$.type", "ARTIST"), consumer_add_artist_to_genre_task)
            .when(sfn.Condition.string_equals("$.type", "ALBUM"), consumer_add_album_to_genre_task)
            .when(sfn.Condition.string_equals("$.type", "SONG"), consumer_add_song_to_genre_task)
            .otherwise(sfn.Fail(self, "UnknownTypeForGenreStepFn",
                                cause="Unsupported event type",
                                error="TypeNotSupported"))
        )

        state_machine_genre = sfn.StateMachine(
            self, "SubscriptionStateMachineGenreSQS",
            definition=definition_genre,
            timeout=Duration.minutes(5)
        )

        genre_sqs_consumer = Function(
            self, "GenreSQSConsumerStepFunction",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/subscription/genre-sqs-consumer"),
            environment={
                "STEP_FUNCTION_ARN": state_machine_genre.state_machine_arn
            }
        )
        state_machine_genre.grant_start_execution(genre_sqs_consumer)
        genre_sqs.grant_consume_messages(genre_sqs_consumer)
        genre_sqs_consumer.add_event_source(SqsEventSource(
            genre_sqs,
            batch_size=5
        ))

        consumer_add_album_to_artist_task = tasks.LambdaInvoke(
            self, "ProcessAlbumForArtist",
            lambda_function=consumer_add_album_to_artist,
            output_path="$.Payload"
        )

        consumer_add_song_to_artist_task = tasks.LambdaInvoke(
            self, "ProcessSongForArtist",
            lambda_function=consumer_add_song_to_artist,
            output_path="$.Payload"
        )

        choice_artist = sfn.Choice(self, "CheckArtistType")
        definition_artist = (
            choice_artist
            .when(sfn.Condition.string_equals("$.type", "ALBUM"), consumer_add_album_to_artist_task)
            .when(sfn.Condition.string_equals("$.type", "SONG"), consumer_add_song_to_artist_task)
            .otherwise(sfn.Fail(self, "UnknownTypeForArtistStepFn",
                                cause="Unsupported event type",
                                error="TypeNotSupported"))
        )

        state_machine_artist = sfn.StateMachine(
            self, "SubscriptionStateMachineArtistSQS",
            definition=definition_artist,
            timeout=Duration.minutes(5)
        )

        artist_sqs_consumer = Function(
            self, "ArtistSQSConsumerStepFunction",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/subscription/artist-sqs-consumer"),
            environment={
                "STEP_FUNCTION_ARN": state_machine_artist.state_machine_arn
            }
        )
        state_machine_artist.grant_start_execution(artist_sqs_consumer)
        artist_sqs.grant_consume_messages(artist_sqs_consumer)
        artist_sqs_consumer.add_event_source(SqsEventSource(
            artist_sqs,
            batch_size=5
        ))

