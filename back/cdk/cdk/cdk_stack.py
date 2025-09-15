import os
from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_s3 as _s3,
    aws_apigateway as apigw,
    aws_dynamodb as _dynamodb, RemovalPolicy, aws_iam as iam,
    # aws_sqs as sqs,
)
from aws_cdk.aws_dynamodb import AttributeType
from constructs import Construct


class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        common_layer = _lambda.LayerVersion(
            self,
            "CommonLayer",
            description="Common Layer Version",
            code=_lambda.Code.from_asset('layers/content-creation-layer'),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_11,],
        )

        self.songs_bucket = _s3.Bucket(
            self,
            "SongsBucketId",
            bucket_name="songs-bucket-cc52025",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
        )

        self.albums_bucket = _s3.Bucket(
            self,
            "AlbumsBucketId",
            bucket_name="albums-bucket-cc52025",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
        )

        self.artists_bucket = _s3.Bucket(
            self,
            "ArtistsBucketId",
            bucket_name="artists-bucket-cc52025",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
        )

        self.dynamodb = _dynamodb.Table(
            self,
            "SongifyDynamo",
            table_name="SongifyDynamo",
            partition_key=_dynamodb.Attribute(
                name="PK",
                type=AttributeType.STRING,
            ),
            sort_key=_dynamodb.Attribute(
                name="SK",
                type=AttributeType.STRING,
            ),
            removal_policy=RemovalPolicy.DESTROY,
        )

        create_content_get_albums_lambda = _lambda.Function(
            self,
            "Content_Creation_GetAlbums",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=_lambda.Code.from_asset(os.path.join(os.getcwd(), "src/feature/content-creation/get-albums")),
            layers=[common_layer],
        )
        self.dynamodb.grant_read_data(create_content_get_albums_lambda)
        self.albums_bucket.grant_read(create_content_get_albums_lambda)

        api = apigw.RestApi(
            self, "SongifyApi",
            rest_api_name="SongifyApi",
            description="This service serves song-related information."
        )
        hello = api.root.add_resource('hello')
        hello.add_method("GET", apigw.LambdaIntegration(create_content_get_albums_lambda))

        self.api_url = api.url
