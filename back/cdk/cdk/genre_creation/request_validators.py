from aws_cdk.aws_apigateway import RestApi


def create_genre_icon_upload_request_validator(api: RestApi):
    return api.add_request_validator(
        "GenreCreationGenreIconUploadRequestValidator",
        validate_request_body=True,
        validate_request_parameters=False
    )
def create_genre_creation_request_validator(api: RestApi):
    return api.add_request_validator(
        "GenreCreationGenreCreationRequestValidator",
        validate_request_body=True,
        validate_request_parameters=False
    )