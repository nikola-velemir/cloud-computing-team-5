from aws_cdk.aws_apigateway import RestApi, Model, JsonSchemaVersion, JsonSchema, JsonSchemaType


def create_genre_icon_upload_request_model(api: RestApi) -> Model:
    return api.add_model(
        "GenreCreationGenreIconUploadRequest",
        content_type="application/json",
        model_name="GenreCreationGenreIconUploadRequest",
        schema=JsonSchema(
            schema=JsonSchemaVersion.DRAFT4,
            title="GenreIconUploadRequest",
            type=JsonSchemaType.OBJECT,
            properties={
                "genreId": JsonSchema(type=JsonSchemaType.STRING),
                "contentType": JsonSchema(type=JsonSchemaType.STRING),
            },
            required=["genreId", "contentType"]
        )
    )
def create_genre_creation_request_model(api: RestApi) -> Model:
    return api.add_model(
        "GenreCreationGenreCreationRequest",
        content_type="application/json",
        model_name="GenreCreationGenreCreationRequest",
        schema=JsonSchema(
            schema=JsonSchemaVersion.DRAFT4,
            title="GenreCreationRequest",
            type=JsonSchemaType.OBJECT,
            properties={
                "name": JsonSchema(type=JsonSchemaType.STRING),
                "description": JsonSchema(type=JsonSchemaType.STRING),
                "imageType": JsonSchema(type=JsonSchemaType.STRING),
            },
            required=["name", "description", "imageType"]
        )
    )