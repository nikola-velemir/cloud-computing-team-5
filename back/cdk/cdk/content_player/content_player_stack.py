import os

from aws_cdk import Stack
from aws_cdk.aws_apigateway import IRestApi, LambdaIntegration, CognitoUserPoolsAuthorizer, AuthorizationType
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_lambda import Function, Runtime, Code, LayerVersion
from aws_cdk.aws_s3 import IBucket
from aws_cdk.aws_sqs import IQueue
from constructs import Construct

from cdk.content_player.request_validators import *
from cdk.content_player.request_models import *
from cdk.cors_helper import add_cors_options


class ContentPlayerStack(Stack):
    def __init__(self, scope: Construct, id: str, *, api: IRestApi, dynamo: ITable, song_bucket: IBucket, region: str,
                 authorizer: CognitoUserPoolsAuthorizer,
                 utils_layer: LayerVersion,
                 feed_sqs: IQueue,
                 **kwargs):
        super().__init__(scope, id, **kwargs)

        content_player_api = api.root.add_resource("content-player")
        add_cors_options(content_player_api)
        get_track_api = content_player_api.add_resource("get-track")
        add_cors_options(get_track_api)
        get_track_by_id_api = get_track_api.add_resource("{id}")
        add_cors_options(get_track_by_id_api)
        get_track_lambda = Function(
            self,
            id="ContentPlayerGetTrack",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), 'src/feature/content-player/get-track')),
            environment={
                "TABLE_NAME": dynamo.table_name,
                "SONGS_BUCKET": song_bucket.bucket_name,
                "EXPIRATION_TIME": '3600',
                "REGION": region,
                "FEED_QUEUE_URL": feed_sqs.queue_url,
            },
            layers=[utils_layer]
        )
        song_bucket.grant_read(get_track_lambda)
        feed_sqs.grant_send_messages(get_track_lambda)
        dynamo.grant_read_data(get_track_lambda)
        get_track_by_id_api.add_method(
            "GET",
            LambdaIntegration(get_track_lambda, proxy=True),
            request_validator=create_get_song_request_validator(api),
            request_parameters=create_get_song_request_params(),
            authorization_type=AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        get_album_api = content_player_api.add_resource("get-album")
        add_cors_options(get_album_api)
        get_album_by_id_api = get_album_api.add_resource("{id}")
        add_cors_options(get_album_by_id_api)
        get_album_lambda = Function(
            self,
            id="ContentPlayerGetAlbum",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset(os.path.join(os.getcwd(), 'src/feature/content-player/get-album')),
            environment={
                "TABLE_NAME": dynamo.table_name,
                "FEED_QUEUE_URL": feed_sqs.queue_url,
            },
            layers=[utils_layer]
        )
        dynamo.grant_read_data(get_album_lambda)
        feed_sqs.grant_send_messages(get_album_lambda)
        get_album_by_id_api.add_method(
            "GET",
            LambdaIntegration(get_album_lambda, proxy=True),
            request_validator=create_get_album_request_validator(api),
            request_parameters=create_get_album_request_params(),
            authorization_type=AuthorizationType.COGNITO,
            authorizer=authorizer
        )
