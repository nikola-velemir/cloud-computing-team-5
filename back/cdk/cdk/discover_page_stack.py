import os

from aws_cdk import Stack
from aws_cdk.aws_apigateway import LambdaIntegration, IRestApi
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_lambda import Function, Runtime, Code, LayerVersion
from aws_cdk.aws_s3 import IBucket
from constructs import Construct

from cdk.cors_helper import add_cors_options


class DiscoverPageStack(Stack):
    def __init__(self, scope: Construct, id: str, api: IRestApi, dynamoDb: ITable, albums_bucket: IBucket, genre_bucket:IBucket,
                 artists_bucket: IBucket, song_bucket: IBucket, **kwargs):
        super().__init__(scope, id, **kwargs)

        discover_page_api = api.root.add_resource("discover-page")

        get_genres_lambda = Function(
            self,
            "Discover_Page_GetGenres",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/discover-page/get-genres")),
            environment={
                "DYNAMO": dynamoDb.table_name,
                "BUCKET": genre_bucket.bucket_name,
                "EXPIRATION_TIME": "1800"
            }
        )
        genre_bucket.grant_read(get_genres_lambda)
        dynamoDb.grant_read_data(get_genres_lambda)
        genres_api = discover_page_api.add_resource("genres")
        genres_api.add_method("GET", LambdaIntegration(get_genres_lambda, proxy=True))
        add_cors_options(genres_api)

        get_albums_lambda = Function(
            self,
            "Discover_Page_GetAlbums",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/discover-page/get-albums")),
            environment={
                "DYNAMO": dynamoDb.table_name,
                "BUCKET": albums_bucket.bucket_name,
                "EXPIRATION_TIME": "1800"
            }
        )
        albums_bucket.grant_read(get_albums_lambda)
        dynamoDb.grant_read_data(get_albums_lambda)
        albums_api = discover_page_api.add_resource("albums")
        albums_api.add_method("GET", LambdaIntegration(get_albums_lambda, proxy=True))
        add_cors_options(albums_api)

        get_artists_lambda = Function(
            self,
            "Discover_Page_GetArtists",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/discover-page/get-artists")),
            environment={
                "DYNAMO": dynamoDb.table_name,
                "BUCKET": artists_bucket.bucket_name,
                "EXPIRATION_TIME": "1800"
            }
        )
        artists_bucket.grant_read(get_artists_lambda)
        dynamoDb.grant_read_data(get_artists_lambda)
        artists_api = discover_page_api.add_resource("artists")
        artists_api.add_method("GET", LambdaIntegration(get_artists_lambda, proxy=True))
        add_cors_options(artists_api)

        get_songs_lambda = Function(
            self,
            "Discover_Page_GetSongs",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/discover-page/get-songs")),
            environment={
                "DYNAMO": dynamoDb.table_name,
                "BUCKET": song_bucket.bucket_name,
                "EXPIRATION_TIME": "1800"
            }
        )
        song_bucket.grant_read(get_songs_lambda)
        dynamoDb.grant_read_data(get_songs_lambda)
        songs_api = discover_page_api.add_resource("songs")
        songs_api.add_method("GET", LambdaIntegration(get_songs_lambda, proxy=True))
        add_cors_options(songs_api)