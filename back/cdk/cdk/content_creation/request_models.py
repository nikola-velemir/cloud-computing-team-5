from aws_cdk.aws_apigateway import RestApi, Model, JsonSchema, JsonSchemaVersion, JsonSchemaType


def create_album_request_model(api: RestApi) -> Model:
    return api.add_model(
        "ContentCreationCreateAlbumRequest",
        content_type="application/json",
        model_name="ContentCreationCreateAlbumRequest",
        schema=JsonSchema(
            schema=JsonSchemaVersion.DRAFT4,
            title='CreateAlbumRequest',
            type=JsonSchemaType.OBJECT,
            properties={
                "genreIds": JsonSchema(
                    type=JsonSchemaType.ARRAY,
                    items=JsonSchema(type=JsonSchemaType.STRING)
                ),
                "title": JsonSchema(type=JsonSchemaType.STRING),
                "artistIds": JsonSchema(
                    type=JsonSchemaType.ARRAY,
                    items=JsonSchema(type=JsonSchemaType.STRING)
                ),
                "releaseDate": JsonSchema(type=JsonSchemaType.STRING),
                "imageType": JsonSchema(type=JsonSchemaType.STRING),
            },
            required=["genreIds", "title", "artistIds", "releaseDate", "imageType"]
        )
    )


def create_song_as_single_request_model(api: RestApi) -> Model:
    return api.add_model(
        "ContentCreationCreateSongAsSingleRequest",
        content_type="application/json",
        model_name="ContentCreationCreateSongAsSingleRequest",
        schema=JsonSchema(
            schema=JsonSchemaVersion.DRAFT4,
            title="CreateSongAsSingleRequest",
            type=JsonSchemaType.OBJECT,
            properties={
                "name": JsonSchema(type=JsonSchemaType.STRING),
                "genreId": JsonSchema(type=JsonSchemaType.STRING),
                "artistIds": JsonSchema(
                    type=JsonSchemaType.ARRAY,
                    items=JsonSchema(type=JsonSchemaType.STRING)
                ),
                "duration": JsonSchema(type=JsonSchemaType.NUMBER),
                "imageType": JsonSchema(type=JsonSchemaType.STRING),
                "audioType": JsonSchema(type=JsonSchemaType.STRING),
            },
            required=["name", "genreId", "artistIds", "duration", "imageType", "audioType"]
        )
    )


def create_song_with_album_request_model(api: RestApi) -> Model:
    return api.add_model(
        "CreateSongWithAlbumRequest",
        content_type="application/json",
        model_name="ContentCreationCreateSongWithAlbumRequest",
        schema=JsonSchema(
            schema=JsonSchemaVersion.DRAFT4,
            title="ContentCreationCreateSongWithAlbumRequest",
            type=JsonSchemaType.OBJECT,
            properties={
                "name": JsonSchema(type=JsonSchemaType.STRING),
                "genreId": JsonSchema(type=JsonSchemaType.STRING),
                "artistIds": JsonSchema(
                    type=JsonSchemaType.ARRAY,
                    items=JsonSchema(type=JsonSchemaType.STRING)
                ),
                "albumId": JsonSchema(type=JsonSchemaType.STRING),
                "imageType": JsonSchema(type=JsonSchemaType.STRING),
                "audioType": JsonSchema(type=JsonSchemaType.STRING),
                "duration": JsonSchema(type=JsonSchemaType.NUMBER),
            },
            required=[
                "name",
                "genreId",
                "artistIds",
                "albumId",
                "imageType",
                "audioType",
                "duration"
            ]
        )
    )


def create_song_upload_request_model(api: RestApi) -> Model:
    return api.add_model(
        "ContentCreationSongUploadRequest",
        content_type="application/json",
        model_name="ContentCreationSongUploadRequest",
        schema=JsonSchema(
            schema=JsonSchemaVersion.DRAFT4,
            title="SongUploadRequest",
            type=JsonSchemaType.OBJECT,
            properties={
                "songId": JsonSchema(type=JsonSchemaType.STRING),
                "contentType": JsonSchema(type=JsonSchemaType.STRING),
                "type": JsonSchema(
                    type=JsonSchemaType.STRING,
                    enum=["cover", "audio"]
                ),
            },
            required=["songId", "contentType", "type"]
        )
    )
def create_album_upload_request_model(api: RestApi) -> Model:
    return api.add_model(
        "ContentCreationAlbumUploadRequest",
        content_type="application/json",
        model_name="ContentCreationAlbumUploadRequest",
        schema=JsonSchema(
            schema=JsonSchemaVersion.DRAFT4,
            title="AlbumUploadRequest",
            type=JsonSchemaType.OBJECT,
            properties={
                "albumId": JsonSchema(type=JsonSchemaType.STRING),
                "contentType": JsonSchema(type=JsonSchemaType.STRING),
            },
            required=["albumId", "contentType"]
        )
    )
def create_get_albums_request_model(api: RestApi) -> Model:
    return api.add_model(
        "ContentCreationGetAlbumsRequestModel",
        content_type="application/json",
        model_name="ContentPlayerGetAlbumsRequestModel",
        schema=JsonSchema(
            schema=JsonSchemaVersion.DRAFT4,
            title="GetAlbumsRequest",
            type=JsonSchemaType.OBJECT,
            properties={
                "artistIds": JsonSchema(
                    type=JsonSchemaType.ARRAY,
                    items=JsonSchema(type=JsonSchemaType.STRING)
                ),
            },
            required=["artistIds"]
        )
    )