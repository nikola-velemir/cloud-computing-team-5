from aws_cdk import Stack, RemovalPolicy
from aws_cdk.aws_s3 import Bucket, CorsRule, HttpMethods
from constructs import Construct


class S3Stack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
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
