from aws_cdk.aws_apigateway import RestApi


def create_get_album_request_validator(api: RestApi):
    return api.add_request_validator(
        "ContentPlayerGetAlbumRequestValidator",
        validate_request_body=False,
        validate_request_parameters=True
    )
def create_get_song_request_validator(api: RestApi):
    return api.add_request_validator(
        "ContentPlayerGetSongRequestValidator",
        validate_request_body=False,
        validate_request_parameters=True
    )
