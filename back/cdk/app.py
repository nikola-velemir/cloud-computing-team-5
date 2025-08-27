#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.api_stack import ApiStack
from cdk.content_creation_stack import ContentCreationStack
from cdk.dynamo_stack import DynamoStack
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
    env=env,
)

app.synth()
