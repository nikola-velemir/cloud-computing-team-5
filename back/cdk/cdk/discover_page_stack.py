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