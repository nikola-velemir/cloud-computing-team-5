import json
import os

from aws_cdk import Stack, RemovalPolicy
from aws_cdk.aws_apigateway import IRestApi, LambdaIntegration
from aws_cdk.aws_dynamodb import Table, Attribute, AttributeType
from aws_cdk.aws_lambda import Function, Runtime, Code, LayerVersion
from constructs import Construct

from cdk.cors_helper import add_cors_options


class ContentReviewStack(Stack):
    def __init__(self, scope: Construct, id: str, *, api: IRestApi, region: str, **kwargs) -> None:
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
            layers=[content_review_layer],
            environment={
                "TABLE_NAME": self.review_db.table_name,
                "REVIEW_TYPES": json.dumps(review_types),
            }
        )
        self.review_db.grant_read_write_data(review_song_lambda)
        song_review_api.add_method("PUT", LambdaIntegration(review_song_lambda, proxy=True));

        get_song_review_lambda = Function(
            self,
            id="ContentReviewsGetSongReview",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-review/song/get-review")),
            layers=[content_review_layer],
            environment={
                "TABLE_NAME": self.review_db.table_name,
                "REVIEW_TYPES": json.dumps(review_types),
            }
        )
        self.review_db.grant_read_data(get_song_review_lambda)
        song_get_review_api = song_review_api.add_resource("{id}")
        add_cors_options(song_get_review_api)
        song_get_review_api.add_method("GET", LambdaIntegration(get_song_review_lambda, proxy=True));

