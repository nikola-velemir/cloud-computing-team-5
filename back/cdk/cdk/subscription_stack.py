import os

from aws_cdk import Stack
from aws_cdk.aws_apigateway import LambdaIntegration, IRestApi
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_lambda import Function, Runtime, Code, LayerVersion, StartingPosition
from aws_cdk.aws_lambda_event_sources import DynamoEventSource, SqsEventSource
from aws_cdk.aws_s3 import IBucket
from aws_cdk.aws_sqs import IQueue
from constructs import Construct
from aws_cdk import aws_iam as iam
from aws_cdk import aws_apigateway as apigw

from cdk.cors_helper import add_cors_options


class SubscriptionStack(Stack):
    def __init__(self, scope: Construct, id: str, api: IRestApi, dynamoDb: ITable, subscriptionDynamoDb: ITable, albums_bucket: IBucket, genre_bucket:IBucket,
                 utils_layer: LayerVersion, artists_bucket: IBucket, song_bucket: IBucket,genre_sqs: IQueue,album_sqs: IQueue,artist_sqs: IQueue,region: str,authorizer: apigw.CognitoUserPoolsAuthorizer, **kwargs):
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

        dynamo_add_album_lambda.add_event_source(
            DynamoEventSource(
                dynamoDb,
                starting_position=StartingPosition.LATEST,
                batch_size=5
            )
        )
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

        dynamo_add_artist_lambda.add_event_source(
            DynamoEventSource(
                dynamoDb,
                starting_position=StartingPosition.LATEST,
                batch_size=5
            )
        )

        # trigger when Artist was added to genre-sqs
        consumer_add_artist_to_genre = Function(
            self,
            "ConsumerAddArtistToGenre",
            handler="lambda.lambda_handler",
            runtime=Runtime.PYTHON_3_11,
            code=Code.from_asset(
                os.path.join(os.getcwd(), "src/feature/subscription/add-artist/consumer/genre-sqs")),
            environment={
                "SUBSCRIPTION_TABLE": subscriptionDynamoDb.table_name,
                "REGION": region
            }
        )
        consumer_add_artist_to_genre.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ses:SendEmail", "ses:SendRawEmail"],
                resources=["*"]
            )
        )
        subscriptionDynamoDb.grant_read_write_data(consumer_add_artist_to_genre)
        genre_sqs.grant_consume_messages(consumer_add_artist_to_genre)
        consumer_add_artist_to_genre.add_event_source(SqsEventSource(genre_sqs))


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
                "REGION": region
            }
        )
        consumer_add_song_to_genre.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ses:SendEmail", "ses:SendRawEmail"],
                resources=["*"]
            )
        )
        subscriptionDynamoDb.grant_read_write_data(consumer_add_song_to_genre)
        genre_sqs.grant_consume_messages(consumer_add_song_to_genre)
        consumer_add_song_to_genre.add_event_source(SqsEventSource(genre_sqs))

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
                "REGION": region
            }
        )
        consumer_add_song_to_album.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ses:SendEmail", "ses:SendRawEmail"],
                resources=["*"]
            )
        )
        subscriptionDynamoDb.grant_read_write_data(consumer_add_song_to_album)
        album_sqs.grant_consume_messages(consumer_add_song_to_album)
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
                "REGION": region
            }
        )
        consumer_add_song_to_artist.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ses:SendEmail", "ses:SendRawEmail"],
                resources=["*"]
            )
        )
        subscriptionDynamoDb.grant_read_write_data(consumer_add_song_to_artist)
        artist_sqs.grant_consume_messages(consumer_add_song_to_artist)
        consumer_add_song_to_artist.add_event_source(SqsEventSource(artist_sqs))

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
                "REGION": region
            }
        )
        consumer_add_album_to_artist.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ses:SendEmail", "ses:SendRawEmail"],
                resources=["*"]
            )
        )
        subscriptionDynamoDb.grant_read_write_data(consumer_add_album_to_artist)
        artist_sqs.grant_consume_messages(consumer_add_album_to_artist)
        consumer_add_album_to_artist.add_event_source(SqsEventSource(artist_sqs))

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
                "REGION": region
            }
        )
        consumer_add_album_to_genre.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ses:SendEmail", "ses:SendRawEmail"],
                resources=["*"]
            )
        )
        subscriptionDynamoDb.grant_read_write_data(consumer_add_album_to_genre)
        genre_sqs.grant_consume_messages(consumer_add_album_to_genre)
        consumer_add_album_to_genre.add_event_source(SqsEventSource(genre_sqs))

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
        add_cors_options(subscribe_api)

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


