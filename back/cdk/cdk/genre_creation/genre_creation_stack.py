from aws_cdk import Stack
from aws_cdk.aws_apigateway import IRestApi, LambdaIntegration, CognitoUserPoolsAuthorizer, AuthorizationType
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_lambda import Function, Runtime, Code, LayerVersion
from aws_cdk.aws_s3 import IBucket
from constructs import Construct

from cdk.genre_creation.request_models import *

from cdk.cors_helper import add_cors_options
from cdk.genre_creation.request_validators import *


class GenreCreationStack(Stack):
    def __init__(self, scope: Construct, id: str, *, api: IRestApi, dynamoDb: ITable, genre_bucket: IBucket,
                 region: str, authorizer: CognitoUserPoolsAuthorizer, utils_layer: LayerVersion,
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
            },
            layers=[utils_layer],
        )
        dynamoDb.grant_write_data(create_genre_metadata)
        genre_creation_api.add_method(
            "POST",
            LambdaIntegration(create_genre_metadata, proxy=True),
            request_models={"application/json": create_genre_creation_request_model(api)},
            request_validator=create_genre_creation_request_validator(api),
            authorization_type=AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        upload_genre_icon = Function(
            self,
            "UploadGenreIcon",
            runtime=Runtime.PYTHON_3_11,
            code=Code.from_asset("src/feature/genre-creation/request-genre-presigned-url"),
            handler="lambda.lambda_handler",
            environment={
                "BUCKET_NAME": genre_bucket.bucket_name,
                "EXPIRATION_TIME": "3600",
                "REGION": region
            }
        )
        genre_bucket.grant_put(upload_genre_icon)
        genre_bucket.grant_read_write(upload_genre_icon)
        genre_creation_api.add_method(
            "PUT",
            LambdaIntegration(upload_genre_icon, proxy=True),
            request_models={"application/json": create_genre_icon_upload_request_model(api)},
            request_validator=create_genre_icon_upload_request_validator(api),
            authorization_type=AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        add_cors_options(genre_creation_api)
