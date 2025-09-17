import json
import os

from aws_cdk import Stack, RemovalPolicy
from aws_cdk.aws_apigateway import IRestApi, LambdaIntegration, CognitoUserPoolsAuthorizer, AuthorizationType
from aws_cdk.aws_dynamodb import Table, Attribute, AttributeType, StreamViewType
from aws_cdk.aws_lambda import Function, Runtime, Code, LayerVersion
from constructs import Construct

from cdk.content_review.request_models import *
from cdk.content_review.request_validators import *
from cdk.cors_helper import add_cors_options


class ContentReviewStack(Stack):
    def __init__(self, scope: Construct, id: str, *, api: IRestApi,
                 region: str,
                 authorizer: CognitoUserPoolsAuthorizer,
                 utils_layer: LayerVersion
                 , **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        review_types = [
            "NONE",
            "LIKE",
            "LOVE",
            "DISLIKE"

        ]
        content_review_layer = LayerVersion(
            self, "ContentReviewLayer",
            code=Code.from_asset("layers/content-review-layer"),
            compatible_runtimes=[Runtime.PYTHON_3_9, Runtime.PYTHON_3_11],
        )
        self.review_db = Table(
            self,
            "SongifyReviews",
            table_name="SongifyReviews",
            partition_key=Attribute(
                name="User",
                type=AttributeType.STRING,
            ),
            sort_key=Attribute(
                name="Content",
                type=AttributeType.STRING,
            ),
            removal_policy=RemovalPolicy.DESTROY,
            stream=StreamViewType.NEW_AND_OLD_IMAGES
        )
        content_review_api = api.root.add_resource("content-reviews")
        add_cors_options(content_review_api)
        song_review_api = content_review_api.add_resource("songs")
        add_cors_options(song_review_api)

        review_song_lambda = Function(
            self,
            id="ContentReviewsSetSongReview",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-review/song/set-review")),
            layers=[content_review_layer, utils_layer],
            environment={
                "TABLE_NAME": self.review_db.table_name,
                "REVIEW_TYPES": json.dumps(review_types),
            },
        )
        self.review_db.grant_read_write_data(review_song_lambda)
        song_review_api.add_method(
            "PUT",
            LambdaIntegration(review_song_lambda, proxy=True),
            request_models={"application/json": create_song_review_request_model(api, review_types)},
            request_validator=create_song_review_request_validator(api),
            authorization_type=AuthorizationType.COGNITO,
            authorizer=authorizer

        );

        get_song_review_lambda = Function(
            self,
            id="ContentReviewsGetSongReview",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-review/song/get-review")),
            layers=[content_review_layer, utils_layer],
            environment={
                "TABLE_NAME": self.review_db.table_name,
                "REVIEW_TYPES": json.dumps(review_types),
            }
        )
        self.review_db.grant_read_data(get_song_review_lambda)
        song_get_review_api = song_review_api.add_resource("{id}")
        add_cors_options(song_get_review_api)
        song_get_review_api.add_method(
            "GET",
            LambdaIntegration(get_song_review_lambda, proxy=True),
            authorizer=authorizer,
            authorization_type=AuthorizationType.COGNITO,

        );

        album_review_api = content_review_api.add_resource("albums")
        add_cors_options(album_review_api)

        review_album_lambda = Function(
            self,
            id="ContentReviewsSetAlbumReview",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-review/album/set-review")),
            layers=[content_review_layer, utils_layer],
            environment={
                "TABLE_NAME": self.review_db.table_name,
                "REVIEW_TYPES": json.dumps(review_types),
            }
        )
        self.review_db.grant_read_write_data(review_album_lambda)
        album_review_api.add_method(
            "PUT",
            LambdaIntegration(review_album_lambda, proxy=True),
            request_models={"application/json": create_album_review_request_model(api, review_types)},
            request_validator=create_album_review_request_validator(api),
            authorization_type=AuthorizationType.COGNITO,
            authorizer=authorizer

        );

        get_album_review_lambda = Function(
            self,
            id="ContentReviewsGetAlbumReview",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-review/album/get-review")),
            layers=[content_review_layer, utils_layer],
            environment={
                "TABLE_NAME": self.review_db.table_name,
                "REVIEW_TYPES": json.dumps(review_types),
            }
        )
        self.review_db.grant_read_data(get_album_review_lambda)
        album_get_review_api = album_review_api.add_resource("{id}")
        add_cors_options(album_get_review_api)
        album_get_review_api.add_method(
            "GET",
            LambdaIntegration(get_album_review_lambda, proxy=True),
            authorization_type=AuthorizationType.COGNITO,
            authorizer=authorizer
        );

        artist_review_api = content_review_api.add_resource("artists")
        add_cors_options(artist_review_api)

        review_artist_lambda = Function(
            self,
            id="ContentReviewsSetArtistReview",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-review/artist/set-review")),
            layers=[content_review_layer, utils_layer],
            environment={
                "TABLE_NAME": self.review_db.table_name,
                "REVIEW_TYPES": json.dumps(review_types),
            }
        )
        self.review_db.grant_read_write_data(review_artist_lambda)
        artist_review_api.add_method(
            "PUT",
            LambdaIntegration(review_artist_lambda, proxy=True),
            request_models={"application/json": create_artist_review_request_model(api, review_types)},
            request_validator=create_artist_review_request_validator(api),
            authorization_type=AuthorizationType.COGNITO,
            authorizer=authorizer
        );
        get_artist_review_lambda = Function(
            self,
            id="ContentReviewsGetArtistReview",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-review/artist/get-review")),
            layers=[content_review_layer, utils_layer],
            environment={
                "TABLE_NAME": self.review_db.table_name,
                "REVIEW_TYPES": json.dumps(review_types),
            }
        )
        self.review_db.grant_read_data(get_artist_review_lambda)
        artist_get_review_api = artist_review_api.add_resource("{id}")
        add_cors_options(artist_get_review_api)
        artist_get_review_api.add_method(
            "GET",
            LambdaIntegration(get_artist_review_lambda, proxy=True),
            authorization_type=AuthorizationType.COGNITO,
            authorizer=authorizer
        );

        genre_review_api = content_review_api.add_resource("genres")
        add_cors_options(genre_review_api)

        review_genre_lambda = Function(
            self,
            id="ContentReviewsSetGenreReview",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-review/genre/set-review")),
            layers=[content_review_layer, utils_layer],
            environment={
                "TABLE_NAME": self.review_db.table_name,
                "REVIEW_TYPES": json.dumps(review_types),
            }
        )
        self.review_db.grant_read_write_data(review_genre_lambda)
        genre_review_api.add_method(
            "PUT",
            LambdaIntegration(review_genre_lambda, proxy=True),
            request_models={"application/json": create_genre_review_request_model(api, review_types)},
            request_validator=create_genre_review_request_validator(api),
            authorizer=authorizer,
            authorization_type=AuthorizationType.COGNITO,
        );

        get_genre_review_lambda = Function(
            self,
            id="ContentReviewsGetGenreReview",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-review/genre/get-review")),
            layers=[content_review_layer, utils_layer],
            environment={
                "TABLE_NAME": self.review_db.table_name,
                "REVIEW_TYPES": json.dumps(review_types),
            }
        )
        self.review_db.grant_read_data(get_genre_review_lambda)
        genre_get_review_api = genre_review_api.add_resource("{id}")
        add_cors_options(genre_get_review_api)
        genre_get_review_api.add_method(
            "GET",
            LambdaIntegration(get_genre_review_lambda, proxy=True),
            authorization_type=AuthorizationType.COGNITO,
            authorizer=authorizer
        );
