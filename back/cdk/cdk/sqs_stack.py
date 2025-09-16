from aws_cdk import (
    Stack,
    aws_sqs as sqs,
    Duration,
)
from constructs import Construct


class SqsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #add song
        #add artist
        #add album
        self.subscription_genre_queue = sqs.Queue(
            self, "SubscriptionGenreQueue",
            queue_name="subscription-genre-queue",
            visibility_timeout=Duration.seconds(30),
            retention_period=Duration.days(4)
        )

        #add song
        #add album
        self.subscription_artist_queue = sqs.Queue(
            self, "SubscriptionArtistQueue",
            queue_name="subscription-artist-queue",
            visibility_timeout=Duration.seconds(30),
            retention_period=Duration.days(4)
        )

        #add song (?)
        self.subscription_album_queue = sqs.Queue(
            self, "SubscriptionAlbumQueue",
            queue_name="subscription-album-queue",
            visibility_timeout=Duration.seconds(30),
            retention_period=Duration.days(4)
        )

