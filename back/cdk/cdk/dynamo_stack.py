from aws_cdk import Stack, RemovalPolicy
from aws_cdk.aws_dynamodb import Table, Attribute, AttributeType, ProjectionType, StreamViewType
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
            stream=StreamViewType.NEW_AND_OLD_IMAGES
        )

        # GSI za dobavljanje svih pojedinacnih entiteta
        # PRIMER:
        # PK:GENRE#247124617418248129847
        # SK:METADATA
        # EntityType: GENRE
        self.dynamodb.add_global_secondary_index(
            index_name="EntitiesIndex",
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

        #PK -> ENTITY#<id>  (ALBUM, SONG, ARTIST, GENRE)
        #SK -> USER#<id>
        self.subscription_db = Table(
            self,
            "SongifySubscription",
            table_name="SongifySubscription",
            partition_key=Attribute(
                name="PK",
                type=AttributeType.STRING,
            ),
            sort_key=Attribute(
                name="SK",
                type=AttributeType.STRING,
            ),
            removal_policy=RemovalPolicy.DESTROY,
            stream=StreamViewType.NEW_AND_OLD_IMAGES
        )

        # GSI za dobavljanje svih pretplata nekog korisnika
        # PRIMER:
        # SK:USER#247124617418248129847
        self.subscription_db.add_global_secondary_index(
            index_name="UsersIndex",
            partition_key=Attribute(
                name="SK",
                type=AttributeType.STRING,
            ),
            projection_type=ProjectionType.ALL
        )

        #PK -> USER#<id>
        #SK -> ENTITY#<id>  (ALBUM, SONG, ARTIST, GENRE)
        self.feed_db = Table(
            self,
            "SongifyFeed",
            table_name="SongifyFeed",
            partition_key=Attribute(
                name="PK",
                type=AttributeType.STRING,
            ),
            sort_key=Attribute(
                name="SK",
                type=AttributeType.STRING,
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        self.feed_db.add_global_secondary_index(
            index_name="ContentsIndex",
            partition_key=Attribute(
                name="SK",
                type=AttributeType.STRING,
            ),
            projection_type=ProjectionType.ALL
        )