import os

from aws_cdk import Stack
from aws_cdk.aws_apigateway import LambdaIntegration, IRestApi
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_lambda import Function, Runtime, Code, LayerVersion
from aws_cdk.aws_s3 import IBucket
from constructs import Construct

from cdk.cors_helper import add_cors_options


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
                "DYNAMO": dynamoDb.table_name,
                "BUCKET": albums_bucket.bucket_name,
                "EXPIRATION_TIME" : "1800"
            }
        )
        albums_bucket.grant_read(get_albums_lambda)
        dynamoDb.grant_read_data(get_albums_lambda)
        #        albums_bucket.grant_read(get_albums_lambda)
        albums_api = content_creation_api.add_resource("albums")
        albums_api.add_method("GET", LambdaIntegration(get_albums_lambda, proxy=True))

        request_presigned_url_album = Function(
            self,
            "Content_Creation_AlbumPresignedUrl",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-creation/request-presigned-url-album")),
            environment={
                "BUCKET_NAME": albums_bucket.bucket_name,
                "EXPIRATION_TIME": '3600'
            })
        albums_bucket.grant_write(request_presigned_url_album)
        albums_api.add_method("PUT", LambdaIntegration(request_presigned_url_album, proxy=True))
        request_presigned_url_song = Function(
            self,
            "Content_Creation_AlbumSongPresignedUrl",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-creation/request-presigned-url-song")),
            environment={
                "BUCKET_NAME": song_bucket.bucket_name,
                "EXPIRATION_TIME": '3600'
            })
        song_bucket.grant_write(request_presigned_url_song)
        song_api = content_creation_api.add_resource('songs')
        song_api.add_method("PUT", LambdaIntegration(request_presigned_url_song, proxy=True))

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

        create_album = Function(
            self,
            id="Content_Creation_CreateAlbum",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-creation/create-album")),
            environment={
                "DYNAMO": dynamoDb.table_name,
            },
        )
        dynamoDb.grant_write_data(create_album)
        albums_api.add_method("POST", LambdaIntegration(create_album, proxy=True))

        create_song_with_album = Function(
            self,
            id="Content_Creation_CreateSongWithAlbum",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-creation/create-song-with-album")),
            environment={
                "DYNAMO": dynamoDb.table_name,
            },
        )
        dynamoDb.grant_write_data(create_song_with_album)
        create_with_album_api = song_api.add_resource("create-with-album")
        create_with_album_api.add_method("POST", LambdaIntegration(create_song_with_album, proxy=True))

        create_song_as_single = Function(
            self,
            id="Content_Creation_CreateSongAsSingle",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-creation/create-song-with-album")),
            environment={
                "DYNAMO": dynamoDb.table_name,
            },
        )
        dynamoDb.grant_write_data(create_song_as_single)
        create_as_single_api = song_api.add_resource("create-as-single")
        create_as_single_api.add_method("POST", LambdaIntegration(create_song_as_single, proxy=True))

        add_cors_options(song_api)
        add_cors_options(albums_api)
        add_cors_options(artists_api)
        add_cors_options(genres_api)
        add_cors_options(create_with_album_api)
        add_cors_options(create_as_single_api)
