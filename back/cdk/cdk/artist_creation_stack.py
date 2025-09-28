
from aws_cdk import Stack
from aws_cdk.aws_apigateway import IRestApi, LambdaIntegration
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_s3 import IBucket
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as _lambda
from constructs import Construct

from cdk.cors_helper import add_cors_options


class ArtistCreationStack(Stack):
    def __init__(self, scope: Construct, construct_id: str,api: IRestApi, dynamoDb: ITable, artist_bucket: IBucket, authorizer: apigw.CognitoUserPoolsAuthorizer,
            utils_layer: _lambda.LayerVersion,**kwargs):
        super().__init__(scope, construct_id, **kwargs)
        artist_creation_api = api.root.add_resource("artist-creation")

        update_genre_lambda = _lambda.Function(
            self, "UpdateGenreLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/artist-creation/update-genre"),
            environment={
                "DYNAMO": dynamoDb.table_name
            },
            layers=[utils_layer],
        )
        dynamoDb.grant_read_write_data(update_genre_lambda)

        # lambda
        create_artist_lambda = _lambda.Function(
            self, "CreateArtistLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/artist-creation/create-artist"),
            environment={
                "DYNAMO": dynamoDb.table_name,
                "BUCKET": artist_bucket.bucket_name,
                "UPDATE_GENRE_LAMBDA_NAME": update_genre_lambda.function_name,
            },
            layers=[utils_layer],
        )

        # permission
        artist_bucket.grant_read(create_artist_lambda)
        dynamoDb.grant_read_data(create_artist_lambda)
        dynamoDb.grant_write_data(create_artist_lambda)
        # invoke update lambda
        update_genre_lambda.grant_invoke(create_artist_lambda)

        # endpoint
        artist_api = artist_creation_api.add_resource("artists")
        artist_api.add_method(
            "POST",
            LambdaIntegration(create_artist_lambda, proxy=True),
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=authorizer,
        )

        add_cors_options(artist_api)