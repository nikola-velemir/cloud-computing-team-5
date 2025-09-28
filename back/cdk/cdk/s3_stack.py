from aws_cdk import Stack, RemovalPolicy, CfnOutput
from aws_cdk.aws_iam import ServicePrincipal, PolicyStatement, Effect
from aws_cdk.aws_lambda import Function, Runtime, Code
from aws_cdk.aws_s3 import Bucket, CorsRule, HttpMethods, EventType, NotificationKeyFilter
from aws_cdk.aws_s3_notifications import LambdaDestination
from constructs import Construct


class S3Stack(Stack):
    def __init__(self, scope: Construct, id: str, *, region: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        cors_rule = CorsRule(
            allowed_methods=[HttpMethods.GET, HttpMethods.PUT, HttpMethods.POST, HttpMethods.HEAD],
            allowed_origins=["*"],
            allowed_headers=["*"],
            exposed_headers=["ETag"],
            max_age=3600,
        )

        self.songs_bucket = Bucket(
            self,
            "SongsBucket",
            bucket_name="cc5-songs-bucket",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
            cors=[cors_rule],
        )
        self.songs_bucket.add_to_resource_policy(
            PolicyStatement(
                principals=[ServicePrincipal("transcribe.amazonaws.com")],
                actions=["s3:GetObject", "s3:PutObject"],
                resources=[f"{self.songs_bucket.bucket_arn}/*"]
            )
        )

        self.albums_bucket = Bucket(
            self,
            "AlbumsBucket",
            bucket_name="cc5-albums-bucket",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
            cors=[cors_rule],
        )

        self.artists_bucket = Bucket(
            self,
            "ArtistsBucket",
            bucket_name="cc5-artists-bucket",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
            cors=[cors_rule],
        )
        self.genre_bucket = Bucket(
            self,
            "GenresBucket",
            bucket_name="cc5-genres-bucket",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
            cors=[cors_rule],
        )
        self.songs_bucket.add_to_resource_policy(
            PolicyStatement(
                principals=[ServicePrincipal("transcribe.amazonaws.com")],
                actions=["s3:GetObject", "s3:PutObject"],
                resources=[f"{self.songs_bucket.bucket_arn}/*"]
            )
        )
        CfnOutput(
            self,
            "SongBucketName",
            value=self.songs_bucket.bucket_name,
            export_name="SongsBucketName"
        )
        CfnOutput(
            self,
            "SongsBucketArn",
            value=self.songs_bucket.bucket_arn,
            export_name="SongsBucketArn"
        )