from aws_cdk import (
    Stack,
)
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_s3 import IBucket
from constructs import Construct


class AudioTranscriptionStack(Stack):
    def __init__(self, scope: Construct, id: str, *, table: ITable, songs_bucket: IBucket, **kwargs):
        super().__init__(scope, id, **kwargs)

