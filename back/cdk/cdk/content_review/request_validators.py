from aws_cdk.aws_apigateway import RestApi

def create_album_review_request_validator(api: RestApi):
    return api.add_request_validator(
        "ContentReviewAlbumIdValidator",
        validate_request_body=True,
        validate_request_parameters=False
    )

def create_genre_review_request_validator(api: RestApi):
    return api.add_request_validator(
        "ContentReviewGenreIdValidator",
        validate_request_body=True,
        validate_request_parameters=False
    )

def create_artist_review_request_validator(api: RestApi):
    return api.add_request_validator(
        "ContentReviewArtistIdValidator",
        validate_request_body=True,
        validate_request_parameters=False
    )

def create_song_review_request_validator(api: RestApi):
    return api.add_request_validator(
        "ContentReviewSongIdValidator",
        validate_request_body=True,
        validate_request_parameters=False
    )
