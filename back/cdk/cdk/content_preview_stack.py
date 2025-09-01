import os

from aws_cdk import Stack
from aws_cdk.aws_apigateway import IRestApi, LambdaIntegration
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_lambda import Function, Code, Runtime
from aws_cdk.aws_s3 import IBucket
from constructs import Construct

from cdk.cors_helper import add_cors_options


class ContentPreviewStack(Stack):
    def __init__(self, scope: Construct, id: str,*,
                 dynamo_table: ITable, song_bucket: IBucket, artists_bucket: IBucket, albums_bucket: IBucket,
                 genre_bucket: IBucket, api: IRestApi, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        content_preview_api = api.root.add_resource('content-preview')
        add_cors_options(content_preview_api)

        song_api = content_preview_api.add_resource('song')
        add_cors_options(song_api)
        song_id_api = song_api.add_resource('{id}')
        add_cors_options(song_id_api)

        preview_song_lamda = Function(
            self,
            "PreviewSongLambda",
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-preview/song/song-preview")),
            runtime=Runtime.PYTHON_3_11,
            environment={
                'DYNAMO': dynamo_table.table_name,
                "SONG_BUCKET": song_bucket.bucket_name,
                "ARTIST_BUCKET": artists_bucket.bucket_name,
                "GENRE_BUCKET": genre_bucket.bucket_name,
                "ALBUM_BUCKET": albums_bucket.bucket_name,
                "EXPIRATION_TIME": "1800"

            }
        )
        dynamo_table.grant_read_data(preview_song_lamda)
        song_bucket.grant_read(preview_song_lamda)
        albums_bucket.grant_read(preview_song_lamda)
        artists_bucket.grant_read(preview_song_lamda)
        genre_bucket.grant_read(preview_song_lamda)

        song_id_api.add_method("GET", LambdaIntegration(preview_song_lamda, proxy=True))

        album_api = content_preview_api.add_resource('album')
        add_cors_options(album_api)
        album_id_api = album_api.add_resource('{id}')
        add_cors_options(album_id_api)

        preview_album_lambda = Function(
            self,
            "PreviewAlbumLambda",
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-preview/album/album-preview")),
            runtime=Runtime.PYTHON_3_11,
            environment={
                'DYNAMO': dynamo_table.table_name,
                "SONG_BUCKET": song_bucket.bucket_name,
                "ARTIST_BUCKET": artists_bucket.bucket_name,
                "GENRE_BUCKET": genre_bucket.bucket_name,
                "ALBUM_BUCKET": albums_bucket.bucket_name,
                "EXPIRATION_TIME": "1800"

            }
        )

        dynamo_table.grant_read_data(preview_album_lambda)
        song_bucket.grant_read(preview_album_lambda)
        albums_bucket.grant_read(preview_album_lambda)
        artists_bucket.grant_read(preview_album_lambda)
        genre_bucket.grant_read(preview_album_lambda)

        album_id_api.add_method("GET", LambdaIntegration(preview_album_lambda, proxy=True))

        artist_api = content_preview_api.add_resource('artist')
        add_cors_options(artist_api)
        artist_by_id_api = artist_api.add_resource('{id}')
        add_cors_options(artist_by_id_api)

        preview_artist_lambda = Function(
            self,
            "PreviewArtistLambda",
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-preview/artist/artist-preview")),
            runtime=Runtime.PYTHON_3_11,
            environment={
                'DYNAMO': dynamo_table.table_name,
                "SONG_BUCKET": song_bucket.bucket_name,
                "ARTIST_BUCKET": artists_bucket.bucket_name,
                "GENRE_BUCKET": genre_bucket.bucket_name,
                "ALBUM_BUCKET": albums_bucket.bucket_name,
                "EXPIRATION_TIME": "1800"

            }
        )

        dynamo_table.grant_read_data(preview_artist_lambda)
        song_bucket.grant_read(preview_artist_lambda)
        albums_bucket.grant_read(preview_artist_lambda)
        artists_bucket.grant_read(preview_artist_lambda)
        genre_bucket.grant_read(preview_artist_lambda)

        artist_by_id_api.add_method("GET", LambdaIntegration(preview_artist_lambda, proxy=True))