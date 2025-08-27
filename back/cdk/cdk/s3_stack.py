from aws_cdk import Stack, RemovalPolicy
from aws_cdk.aws_s3 import Bucket
from constructs import Construct


class S3Stack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.songs_bucket = Bucket(
            self,
            "SongsBucket",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
        )

        self.albums_bucket = Bucket(
            self,
            "AlbumsBucket",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
        )

        self.artists_bucket = Bucket(
            self,
            "ArtistsBucket",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
        )
