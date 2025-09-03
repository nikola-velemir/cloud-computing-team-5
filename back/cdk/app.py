#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.api_stack import ApiStack
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
api_stack = ApiStack(app, "ApiStack", env=env)
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
