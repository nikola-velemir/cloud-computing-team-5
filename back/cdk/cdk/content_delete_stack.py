from aws_cdk import Stack
from aws_cdk.aws_apigateway import IRestApi, LambdaIntegration
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_s3 import IBucket
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as _lambda
from constructs import Construct

from cdk.cors_helper import add_cors_options


class ContentDeleteStack(Stack):
    def __init__(self, scope: Construct, id: str,api: IRestApi, dynamoDb: ITable,
                 subscriptionDynamoDb: ITable,
                 reviewDynamoDb: ITable, feedDynamoDb: ITable,
                 authorizer: apigw.CognitoUserPoolsAuthorizer,
                 utils_layer: _lambda.LayerVersion,**kwargs):
        super().__init__(scope, id, **kwargs)
        content_delete_api = api.root.add_resource("content-delete")


        delete_artist_from_albums = _lambda.Function(
            self,
            "DeleteArtistFromAlbumLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/content-delete/artist/delete-from-albums"),
            environment={
                "DYNAMO": dynamoDb.table_name
            },
            layers=[utils_layer],
        )
        delete_artist_from_feed = _lambda.Function(
            self,
            "DeleteArtistFromFeedLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/content-delete/artist/delete-from-feed"),
            environment={
                "DYNAMO": feedDynamoDb.table_name
            },
            layers=[utils_layer],
        )
        delete_artist_from_genres = _lambda.Function(
            self,
            "DeleteArtistFromGenreLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/content-delete/artist/delete-from-genres"),
            environment={
                "DYNAMO": dynamoDb.table_name,
            },
            layers=[utils_layer],
        )
        delete_artist_from_reviews = _lambda.Function(
            self,
            "DeleteArtistFromReviewsLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/content-delete/artist/delete-from-reviews"),
            environment={
                "DYNAMO": reviewDynamoDb.table_name
            },
            layers=[utils_layer],
        )
        delete_artist_from_songs = _lambda.Function(
            self,
            "DeleteArtistFromSongsLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/content-delete/artist/delete-from-songs"),
            environment={
                "DYNAMO": dynamoDb.table_name
            },
            layers=[utils_layer],
        )
        delete_artist_from_subscriptions = _lambda.Function(
            self,
            "DeleteArtistFromSubscriptionsLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/content-delete/artist/delete-from-subscriptions"),
            environment={
                "DYNAMO": subscriptionDynamoDb.table_name
            },
            layers=[utils_layer],
        )



        delete_artist_lambda = _lambda.Function(
            self,
            "DeleteArtistLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/content-delete/artist/delete-metadata"),
            environment={
                "DYNAMO": dynamoDb.table_name,
                "DELETE_FROM_ALBUMS_LAMBDA_NAME": delete_artist_from_albums.function_name,
                "DELETE_FROM_FEED_LAMBDA_NAME": delete_artist_from_feed.function_name,
                "DELETE_FROM_GENRES_LAMBDA_NAME": delete_artist_from_genres.function_name,
                "DELETE_FROM_REVIEWS_LAMBDA_NAME": delete_artist_from_reviews.function_name,
                "DELETE_FROM_SONGS_LAMBDA_NAME": delete_artist_from_songs.function_name,
                "DELETE_FROM_SUBSCRIPTIONS_LAMBDA_NAME": delete_artist_from_subscriptions.function_name,
            },
            layers=[utils_layer],
        )
        dynamoDb.grant_read_write_data(delete_artist_lambda)
        dynamoDb.grant_read_write_data(delete_artist_from_albums)
        feedDynamoDb.grant_read_write_data(delete_artist_from_feed)
        dynamoDb.grant_read_write_data(delete_artist_from_genres)
        reviewDynamoDb.grant_read_write_data(delete_artist_from_reviews)
        dynamoDb.grant_read_write_data(delete_artist_from_songs)
        subscriptionDynamoDb.grant_read_write_data(delete_artist_from_subscriptions)

        delete_artist_from_albums.grant_invoke(delete_artist_lambda)
        delete_artist_from_feed.grant_invoke(delete_artist_lambda)
        delete_artist_from_genres.grant_invoke(delete_artist_lambda)
        delete_artist_from_reviews.grant_invoke(delete_artist_lambda)
        delete_artist_from_songs.grant_invoke(delete_artist_lambda)
        delete_artist_from_subscriptions.grant_invoke(delete_artist_lambda)

        artist_resource = content_delete_api.add_resource("artist").add_resource("{id}")
        artist_resource.add_method(
            "DELETE",
            LambdaIntegration(delete_artist_lambda, proxy=True),
            authorizer=authorizer,
            authorization_type=apigw.AuthorizationType.COGNITO
        )

        add_cors_options(artist_resource)


