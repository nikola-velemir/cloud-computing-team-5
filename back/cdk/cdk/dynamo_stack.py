from aws_cdk import Stack, RemovalPolicy
from aws_cdk.aws_dynamodb import Table, Attribute, AttributeType, ProjectionType
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
            removal_policy=RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE,
        )

        #GSI za dobavljanje svih albuma
        #PRIMER:
        # PK:ALBUM#247124617418248129847
        # SK:METADATA
        # EntityType: ALBUM
        self.dynamodb.add_global_secondary_index(
            index_name="AlbumsIndex",
            partition_key=Attribute(
                name="EntityType",
                type=AttributeType.STRING,
            ),
            sort_key=Attribute(
                name="SK",
                type=AttributeType.STRING,
            ),
            projection_type=ProjectionType.ALL
        )

        # GSI za dobavljanje svih umetnika
        # PRIMER:
        # PK:ARTIST#247124617418248129847
        # SK:METADATA
        # EntityType: ARTIST
        self.dynamodb.add_global_secondary_index(
            index_name="ArtistsIndex",
            partition_key=Attribute(
                name="EntityType",
                type=AttributeType.STRING,
            ),
            sort_key=Attribute(
                name="SK",
                type=AttributeType.STRING,
            ),
            projection_type=ProjectionType.ALL
        )
