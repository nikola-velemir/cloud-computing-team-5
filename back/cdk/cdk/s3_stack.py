from aws_cdk import Stack, RemovalPolicy
from aws_cdk.aws_s3 import Bucket, CorsRule, HttpMethods
from constructs import Construct


class S3Stack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        cors_rule = CorsRule(
            allowed_methods=[HttpMethods.GET, HttpMethods.PUT, HttpMethods.POST, HttpMethods.HEAD],
            allowed_origins=["http://localhost:4200"],
            allowed_headers=["*"],
            exposed_headers=["ETag"],
        )

        self.songs_bucket = Bucket(
            self,
            "SongsBucket",
            versioned=False,
            removal_policy=RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE,
            cors=[cors_rule],
        )

        self.albums_bucket = Bucket(
            self,
            "AlbumsBucket",
            versioned=False,
            removal_policy=RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE,
            cors=[cors_rule],
        )

        self.artists_bucket = Bucket(
            self,
            "ArtistsBucket",
            versioned=False,
            removal_policy=RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE,
            cors=[cors_rule],
        )
        self.genre_bucket = Bucket(
            self,
            "GenresBucket",
            versioned=False,
            removal_policy=RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE,
            cors=[cors_rule],
        )
