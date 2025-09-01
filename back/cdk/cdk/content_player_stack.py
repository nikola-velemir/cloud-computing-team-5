from aws_cdk import Stack
from aws_cdk.aws_apigateway import IRestApi
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_s3 import IBucket
from constructs import Construct


class ContentPlayerStack(Stack):
    def __init__(self, scope: Construct, id: str, *, api: IRestApi, dynamo: ITable, song_bucket: IBucket, **kwargs):
        super().__init__(scope, id, **kwargs)

        api.root.add_resource("content-player")
