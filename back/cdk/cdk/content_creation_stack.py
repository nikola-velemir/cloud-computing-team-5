import os

from aws_cdk import Stack, PhysicalName, Fn
from aws_cdk.aws_apigateway import RestApi, LambdaIntegration, IRestApi
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_iam import Role, ServicePrincipal
from aws_cdk.aws_lambda import Function, Runtime, Code, LayerVersion
from aws_cdk.aws_s3 import IBucket
from constructs import Construct


class ContentCreationStack(Stack):
    def __init__(self, scope: Construct, id: str, api: IRestApi, dynamoDb: ITable, albums_bucket: IBucket,
                 artists_bucket: IBucket, song_bucket: IBucket, **kwargs):
        super().__init__(scope, id, **kwargs)

        content_creation_api = api.root.add_resource("content-creation")

        layer = LayerVersion(
            self,
            "CommonLayer",
            description="Common Layer Version",
            code=Code.from_asset('layers/content-creation-layer'),
            compatible_runtimes=[Runtime.PYTHON_3_11, ],
        )
        get_albums_lambda = Function(
            self,
            "Content_Creation_GetAlbums",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-creation/get-albums")),
            environment={
                "DYNAMO": dynamoDb.table_name
            }
        )
        dynamoDb.grant_read_data(get_albums_lambda)
        #        albums_bucket.grant_read(get_albums_lambda)
        albums_api = content_creation_api.add_resource("albums")
        albums_api.add_method("GET", LambdaIntegration(get_albums_lambda, proxy=True))

        get_genres_lamba = Function(
            self,
            id="Content_Creation_GetGenres",
            runtime=Runtime.PYTHON_3_11,
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-creation/get-genres")),
            handler="lambda.lambda_handler",
            environment={
                "DYNAMO": dynamoDb.table_name
            }
        )
        dynamoDb.grant_read_data(get_genres_lamba)
        genres_api = content_creation_api.add_resource("genres")
        genres_api.add_method("GET", LambdaIntegration(get_genres_lamba, proxy=True))

        get_artists_lambda = Function(
            self,
            id="Content_Creation_GetArtists",
            runtime=Runtime.PYTHON_3_11,
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-creation/get-artists")),
            handler="lambda.lambda_handler",
            environment={
                "DYNAMO": dynamoDb.table_name
            }

        )
        dynamoDb.grant_read_data(get_artists_lambda)
        #   artists_bucket.grant_read(get_artists_lambda)
        artists_api = content_creation_api.add_resource("artists")
        artists_api.add_method("GET", LambdaIntegration(get_artists_lambda, proxy=True))

        create_song_with_album = Function(
            self,
            id="Content_Creation_CreateSongWithAlbum",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-creation/create-song-with-album")),
            environment={
                "SONGS_BUCKET": song_bucket.bucket_name,
                "DYNAMO": dynamoDb.table_name,
            },
            layers=[layer]
        )
        dynamoDb.grant_write_data(create_song_with_album)
        song_bucket.grant_write(create_song_with_album)
        songs_api = content_creation_api.add_resource("songs")
        songs_api.add_method("POST", LambdaIntegration(create_song_with_album, proxy=True))
