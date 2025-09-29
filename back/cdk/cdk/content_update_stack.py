from aws_cdk import Stack
from aws_cdk.aws_apigateway import IRestApi, LambdaIntegration
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_s3 import IBucket
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as _lambda
from constructs import Construct

from cdk.cors_helper import add_cors_options


class ContentUpdateStack(Stack):
    def __init__(self, scope: Construct, construct_id: str,api: IRestApi, dynamoDb: ITable,
                 subscriptionDynamoDb: ITable,
                 reviewDynamoDb: ITable,
                 feedDynamoDb: ITable,
                 artist_bucket: IBucket, authorizer: apigw.CognitoUserPoolsAuthorizer,
            utils_layer: _lambda.LayerVersion,**kwargs):
        super().__init__(scope, construct_id, **kwargs)
        content_update_api = api.root.add_resource("content-update")


        add_artist_to_genres = _lambda.Function(
            self,
            "AddArtistToGenresLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/content-update/artist/add-artist-to-genres"),
            environment={
                "DYNAMO": dynamoDb.table_name
            },
            layers=[utils_layer],
        )
        remove_artist_from_genres = _lambda.Function(
            self,
            "RemoveArtistFromGenresLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/content-update/artist/remove-artist-from-genres"),
            environment={
                "DYNAMO": dynamoDb.table_name
            },
            layers=[utils_layer],
        )
        update_artist_in_albums = _lambda.Function(
            self,
            "UpdateArtistInAlbumsLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/content-update/artist/update-artist-in-albums"),
            environment={
                "DYNAMO": dynamoDb.table_name
            },
            layers=[utils_layer],
        )
        update_artist_in_feed = _lambda.Function(
            self,
            "UpdateArtistInFeedLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/content-update/artist/update-artist-in-feed"),
            environment={
                "DYNAMO": feedDynamoDb.table_name
            },
            layers=[utils_layer],
        )
        update_artist_in_genres = _lambda.Function(
            self,
            "UpdateArtistInGenresLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/content-update/artist/update-artist-in-genres"),
            environment={
                "DYNAMO": dynamoDb.table_name
            },
            layers=[utils_layer],
        )
        update_artist_in_reviews = _lambda.Function(
            self,
            "UpdateArtistInReviewsLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/content-update/artist/update-artist-in-reviews"),
            environment={
                "DYNAMO": reviewDynamoDb.table_name
            },
            layers=[utils_layer],
        )
        update_artist_in_songs = _lambda.Function(
            self,
            "UpdateArtistInSongsLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/content-update/artist/update-artist-in-songs"),
            environment={
                "DYNAMO": dynamoDb.table_name
            },
            layers=[utils_layer],
        )
        update_artist_in_subscriptions = _lambda.Function(
            self,
            "UpdateArtistInSubscriptionsLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/content-update/artist/update-artist-in-subscriptions"),
            environment={
                "DYNAMO": subscriptionDynamoDb.table_name
            },
            layers=[utils_layer],
        )

        update_artist_lambda = _lambda.Function(
            self, "UpdateArtistLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset("src/feature/content-update/artist/update-artist-metadata"),
            environment={
                "DYNAMO": dynamoDb.table_name,
                "ADD_ARTIST_TO_GENRES": add_artist_to_genres.function_name,
                "REMOVE_ARTIST_FROM_GENRES": remove_artist_from_genres.function_name,
                "UPDATE_ARTIST_IN_ALBUMS": update_artist_in_albums.function_name,
                "UPDATE_ARTIST_IN_FEED": update_artist_in_feed.function_name,
                "UPDATE_ARTIST_IN_GENRES": update_artist_in_genres.function_name,
                "UPDATE_ARTIST_IN_REVIEWS": update_artist_in_reviews.function_name,
                "UPDATE_ARTIST_IN_SONGS": update_artist_in_songs.function_name,
                "UPDATE_ARTIST_IN_SUBSCRIPTIONS": update_artist_in_subscriptions.function_name,
            },
            layers=[utils_layer],
        )

        # permission
        dynamoDb.grant_read_write_data(update_artist_lambda)

        dynamoDb.grant_read_write_data(add_artist_to_genres)
        dynamoDb.grant_read_write_data(remove_artist_from_genres)
        dynamoDb.grant_read_write_data(update_artist_in_albums)
        feedDynamoDb.grant_read_write_data(update_artist_in_feed)
        dynamoDb.grant_read_write_data(update_artist_in_genres)
        reviewDynamoDb.grant_read_write_data(update_artist_in_reviews)
        dynamoDb.grant_read_write_data(update_artist_in_songs)
        subscriptionDynamoDb.grant_read_write_data(update_artist_in_subscriptions)

        # invoke update lambda
        add_artist_to_genres.grant_invoke(update_artist_lambda)
        remove_artist_from_genres.grant_invoke(update_artist_lambda)
        update_artist_in_albums.grant_invoke(update_artist_lambda)
        update_artist_in_feed.grant_invoke(update_artist_lambda)
        update_artist_in_genres.grant_invoke(update_artist_lambda)
        update_artist_in_reviews.grant_invoke(update_artist_lambda)
        update_artist_in_songs.grant_invoke(update_artist_lambda)
        update_artist_in_subscriptions.grant_invoke(update_artist_lambda)


        # endpoint
        artist_api = content_update_api.add_resource("artist")
        artist_api.add_method(
            "POST",
            LambdaIntegration(update_artist_lambda, proxy=True),
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=authorizer,
        )

        add_cors_options(artist_api)
