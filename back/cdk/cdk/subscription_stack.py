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

from cdk.cors_helper import add_cors_options


class SubscriptionStack(Stack):
    def __init__(self, scope: Construct, id: str, api: IRestApi, dynamoDb: ITable, subscriptionDynamoDb: ITable, albums_bucket: IBucket, genre_bucket:IBucket,
                 artists_bucket: IBucket, song_bucket: IBucket,genre_sqs: IQueue,album_sqs: IQueue,artist_sqs: IQueue,region: str, **kwargs):
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

        # trigger when something was added to genre_sqs
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

        # trigger when something was added to album
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

        # trigger when something was added to artist_sqs
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


