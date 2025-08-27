from aws_cdk import Stack, RemovalPolicy
from aws_cdk.aws_dynamodb import Table, Attribute, AttributeType
from constructs import Construct


class DynamoStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.dynamodb = Table(
            self,
            "SongifyDynamo",
            table_name="SongifyDynamo",
            partition_key=Attribute(
                name="PK",
                type=AttributeType.STRING,
            ),
            sort_key=Attribute(
                name="SK",
                type=AttributeType.STRING,
            ),
            removal_policy=RemovalPolicy.DESTROY,
        )
