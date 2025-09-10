from aws_cdk import Stack
from aws_cdk.aws_apigateway import IRestApi, LambdaIntegration
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_lambda import Function, Runtime, Code, LayerVersion
from aws_cdk.aws_s3 import IBucket
from constructs import Construct

from cdk.cors_helper import add_cors_options


class GenreCreationStack(Stack):
    def __init__(self, scope: Construct, id: str, api: IRestApi, dynamoDb: ITable, genre_bucket: IBucket,
                 **kwargs):
        super().__init__(scope, id, **kwargs)
        genre_creation_api = api.root.add_resource("genre-creation")



        create_genre_metadata = Function(
            self,
            "CreateGenreMetadata",
            runtime=Runtime.PYTHON_3_11,
            code=Code.from_asset("src/feature/genre-creation/create-genre"),
            handler="lambda.lambda_handler",
            environment={
                "DYNAMO": dynamoDb.table_name
            }
        )
        dynamoDb.grant_write_data(create_genre_metadata)
        genre_creation_api.add_method("POST", LambdaIntegration(create_genre_metadata, proxy=True))

        upload_genre_icon = Function(
            self,
            "UploadGenreIcon",
            runtime=Runtime.PYTHON_3_11,
            code=Code.from_asset("src/feature/genre-creation/request-genre-presigned-url"),
            handler="lambda.lambda_handler",
            environment={
                "BUCKET_NAME": genre_bucket.bucket_name,
                "EXPIRATION_TIME": "3600"
            }
        )
        genre_bucket.grant_put(upload_genre_icon)
        genre_bucket.grant_read_write(upload_genre_icon)
        genre_creation_api.add_method("PUT", LambdaIntegration(upload_genre_icon, proxy=True))

        add_cors_options(genre_creation_api)