from aws_cdk.aws_apigateway import RestApi


def create_album_request_validator(api: RestApi):
    return api.add_request_validator(
        "ContentCreationCreateAlbumRequestValidator",
        validate_request_body=True,
        validate_request_parameters=False
    )


def create_song_as_single_request_validator(api: RestApi):
    return api.add_request_validator(
        "ContentCreationCreateSongAsSingleRequestValidator",
        validate_request_body=True,
        validate_request_parameters=False
    )


def create_song_with_album_request_validator(api: RestApi):
    return api.add_request_validator(
        "ContentCreationCreateSongWithAlbumRequestValidator",
        validate_request_body=True,
        validate_request_parameters=False
    )


def create_song_upload_request_validator(api: RestApi):
    return api.add_request_validator(
        "ContentCreationSongUploadRequestValidator",
        validate_request_body=True,
        validate_request_parameters=False
    )

def create_album_upload_request_validator(api: RestApi):
    return api.add_request_validator(
        "ContentCreationAlbumUploadRequestValidator",
        validate_request_body=True,
        validate_request_parameters=False
    )
def create_get_all_albums_request_validator(api: RestApi):
    return api.add_request_validator(
        "ContentCreationGetAllAlbumsRequestValidator",
        validate_request_body=True,
        validate_request_parameters=False
    )