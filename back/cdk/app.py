#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk.aws_apigateway import IAuthorizer

from cdk.api_cognito_stack import ApiCognitoStack
from cdk.content_delete_stack import ContentDeleteStack
from cdk.feed_stack import FeedStack
from cdk.sqs_stack import SqsStack
from cdk.subscription_stack import SubscriptionStack
from cdk.s3_stack import S3Stack
from cdk.util_stack import UtilStack
from cdk.api_stack import ApiStack

from cdk.artist_creation_stack import ArtistCreationStack
from cdk.content_review.content_review_stack import ContentReviewStack
from cdk.discover_page_stack import DiscoverPageStack
from cdk.content_player.content_player_stack import ContentPlayerStack
from cdk.content_preview.content_preview_stack import ContentPreviewStack
from cdk.home_page_stack import HomePageStack
from cdk.content_creation.content_creation_stack import ContentCreationStack
from cdk.dynamo_stack import DynamoStack
from cdk.genre_creation.genre_creation_stack import GenreCreationStack
REGION = 'eu-central-1'
app = cdk.App()
env = cdk.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=REGION,
)

dynamo_stack = DynamoStack(app, "DynamoStack", env=env)
sqs_stack = SqsStack(app, "SqsStack", env=env)
s3_stack = S3Stack(app, "S3Stack", env=env)
cognito_stack = ApiCognitoStack(app, "CognitoStack", env=env)
utils_layer_stack = UtilStack(app, "UtilsStack", env=env)
api_stack = ApiStack(app, "ApiStack", cognito_stack.user_pool, env=env)

content_creation_stack = ContentCreationStack(
    scope=app,
    id="ContentCreationStack",
    api=api_stack.api,
    dynamoDb=dynamo_stack.dynamodb,
    albums_bucket=s3_stack.albums_bucket,
    artists_bucket=s3_stack.artists_bucket,
    song_bucket=s3_stack.songs_bucket,
    genre_bucket=s3_stack.genre_bucket,
    region=REGION,
    authorizer = api_stack.authorizer,
    utils_layer=utils_layer_stack.utils_layer,
    env=env,
)
genre_creation_stack = GenreCreationStack(
    scope=app,
    id="GenreCreationStack",
    api=api_stack.api,
    dynamoDb=dynamo_stack.dynamodb,
    genre_bucket=s3_stack.genre_bucket,
    region=REGION,
    authorizer = api_stack.authorizer,
    utils_layer=utils_layer_stack.utils_layer,
    env=env
)
artist_creation_stack = ArtistCreationStack(scope=app,
                                            construct_id="ArtistCreationStack",
                                            api=api_stack.api,
                                            dynamoDb=dynamo_stack.dynamodb,
                                            artist_bucket=s3_stack.artists_bucket,
                                            authorizer=api_stack.authorizer,
                                            utils_layer=utils_layer_stack.utils_layer,
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
    region=REGION,
    authorizer = api_stack.authorizer,
    utils_layer=utils_layer_stack.utils_layer,
    env=env
)

content_player_stack = ContentPlayerStack(
    scope=app,
    id="ContentPlayerStack",
    api=api_stack.api,
    song_bucket=s3_stack.songs_bucket,
    dynamo=dynamo_stack.dynamodb,
    region=REGION,
    authorizer = api_stack.authorizer,
    utils_layer=utils_layer_stack.utils_layer,
    feed_sqs=sqs_stack.feed_queue,
    env=env
)
content_review_stack = ContentReviewStack(
    scope=app,
    id="ContentReviewStack",
    env=env,
    api=api_stack.api,
    region=REGION,
    authorizer = api_stack.authorizer,
    utils_layer=utils_layer_stack.utils_layer,
)

subscription_stack = SubscriptionStack(
    scope=app,
    id="SubscriptionStack",
    api=api_stack.api,
    dynamoDb=dynamo_stack.dynamodb,
    subscriptionDynamoDb=dynamo_stack.subscription_db,
    utils_layer=utils_layer_stack.utils_layer,
    artist_sqs=sqs_stack.subscription_artist_queue,
    genre_sqs=sqs_stack.subscription_genre_queue,
    album_sqs=sqs_stack.subscription_album_queue,
    authorizer=api_stack.authorizer,
    feed_sqs=sqs_stack.feed_queue,
    region=REGION,
    env=env
)
feed_stack = FeedStack(
scope=app,
    id="FeedStack",
    api=api_stack.api,
    dynamoDb=dynamo_stack.dynamodb,
    subscriptionDynamoDb=dynamo_stack.subscription_db,
    reviewDynamoDb=content_review_stack.review_db,
    feedDynamoDb=dynamo_stack.feed_db,
    feed_sqs=sqs_stack.feed_queue,
    region=REGION,
    utils_layer=utils_layer_stack.utils_layer,
    authorizer=api_stack.authorizer,
    genre_bucket=s3_stack.genre_bucket,
    albums_bucket=s3_stack.albums_bucket,
    artists_bucket=s3_stack.artists_bucket,
    song_bucket=s3_stack.songs_bucket,
    env=env
)
content_delete_stack = ContentDeleteStack(
    scope=app,
    id="ContentDeleteStack",
    api=api_stack.api,
    dynamoDb=dynamo_stack.dynamodb,
    subscriptionDynamoDb=dynamo_stack.subscription_db,
    reviewDynamoDb=content_review_stack.review_db,
    feedDynamoDb=dynamo_stack.feed_db,
    authorizer=api_stack.authorizer,
    utils_layer=utils_layer_stack.utils_layer,
    env=env
)
app.synth()
