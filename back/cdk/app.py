#!/usr/bin/env python3
import os
from inspect import stack

import aws_cdk as cdk

from cdk.api_cognito_stack import ApiCognitoStack
from cdk.util_stack import UtilStack
from cdk.api_stack import ApiStack
from cdk.artist_creation_stack import ArtistCreationStack
from cdk.discover_page_stack import DiscoverPageStack
from cdk.content_player_stack import ContentPlayerStack
from cdk.content_preview_stack import ContentPreviewStack
from cdk.home_page_stack import HomePageStack
from cdk.content_creation_stack import ContentCreationStack
from cdk.dynamo_stack import DynamoStack
from cdk.genre_creation_stack import GenreCreationStack
from cdk.s3_stack import S3Stack

app = cdk.App()
env = cdk.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region="eu-central-1",
)

dynamo_stack = DynamoStack(app, "DynamoStack", env=env)
s3_stack = S3Stack(app, "S3Stack", env=env)
cognito_stack = ApiCognitoStack(app, "CognitoStack", env=env)
utils_layer_stack = UtilStack(app, "UtilsStack", env=env)
api_stack = ApiStack(app, "ApiStack", cognito_stack.user_pool, jwt_layer=utils_layer_stack.requests_layer, env=env)

content_creation_stack = ContentCreationStack(
    scope=app,
    id="ContentCreationStack",
    api=api_stack.api,
    dynamoDb=dynamo_stack.dynamodb,
    albums_bucket=s3_stack.albums_bucket,
    artists_bucket=s3_stack.artists_bucket,
    song_bucket=s3_stack.songs_bucket,
    genre_bucket=s3_stack.genre_bucket,
    env=env,
)
genre_creation_stack = GenreCreationStack(
    scope=app,
    id="GenreCreationStack",
    api=api_stack.api,
    dynamoDb=dynamo_stack.dynamodb,
    genre_bucket=s3_stack.genre_bucket,
    env=env
)
artist_creation_stack = ArtistCreationStack(scope=app,
                                            construct_id="ArtistCreationStack",
                                            api=api_stack.api,
                                            dynamoDb=dynamo_stack.dynamodb,
                                            artist_bucket=s3_stack.artists_bucket,
                                            authorizer=api_stack.authorizer,
                                            utils_layer=utils_layer_stack.utils_layer,
                                            jwt_layer=utils_layer_stack.requests_layer,
                                            env=env)

home_page_stack = HomePageStack(
    scope=app,
    id="HomePageStack",
    api=api_stack.api,
    dynamoDb=dynamo_stack.dynamodb,
    albums_bucket=s3_stack.albums_bucket,
    artists_bucket=s3_stack.artists_bucket,
    song_bucket=s3_stack.songs_bucket,
    genre_bucket=s3_stack.genre_bucket,
    env=env,
)

discove_page_stack = DiscoverPageStack(
    scope=app,
    id="DiscoverPageStack",
    api=api_stack.api,
    dynamoDb=dynamo_stack.dynamodb,
    albums_bucket=s3_stack.albums_bucket,
    artists_bucket=s3_stack.artists_bucket,
    song_bucket=s3_stack.songs_bucket,
    genre_bucket=s3_stack.genre_bucket,
    env=env,
)
content_preview_stack = ContentPreviewStack(
    scope=app,
    id="ContentPreviewStack",
    api=api_stack.api,
    genre_bucket=s3_stack.genre_bucket,
    albums_bucket=s3_stack.albums_bucket,
    dynamo_table=dynamo_stack.dynamodb,
    song_bucket=s3_stack.songs_bucket,
    artists_bucket=s3_stack.artists_bucket,
    env=env
)

content_player_stack = ContentPlayerStack(
    scope=app,
    id="ContentPlayerStack",
    api=api_stack.api,
    song_bucket=s3_stack.songs_bucket,
    dynamo=dynamo_stack.dynamodb,
    env=env
)

app.synth()
