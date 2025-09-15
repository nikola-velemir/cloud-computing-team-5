from aws_cdk.aws_apigateway import RestApi, Model, JsonSchema, JsonSchemaType, JsonSchemaVersion

def create_album_review_request_model(api: RestApi, review_types:[str]) -> Model:
    return api.add_model(
        "ContentReviewAlbumReviewRequestModel",
        content_type="application/json",
        model_name="ContentReviewAlbumReviewRequestModel",
        schema=JsonSchema(
            schema=JsonSchemaVersion.DRAFT4,
            title="AlbumReviewRequest",
            type=JsonSchemaType.OBJECT,
            properties={
                "albumId": JsonSchema(type=JsonSchemaType.STRING),
                "reviewType": JsonSchema(
                    type=JsonSchemaType.STRING,
                    enum=review_types
                ),
            },
            required=["albumId", "reviewType"]
        )
    )

def create_genre_review_request_model(api: RestApi, review_types:[str]) -> Model:
    return api.add_model(
        "ContentReviewGenreReviewRequestModel",
        content_type="application/json",
        model_name="ContentReviewGenreReviewRequestModel",
        schema=JsonSchema(
            schema=JsonSchemaVersion.DRAFT4,
            title="GenreReviewRequest",
            type=JsonSchemaType.OBJECT,
            properties={
                "genreId": JsonSchema(type=JsonSchemaType.STRING),
                "reviewType": JsonSchema(
                    type=JsonSchemaType.STRING,
                    enum=review_types
                ),
            },
            required=["genreId", "reviewType"]
        )
    )

def create_artist_review_request_model(api: RestApi, review_types:[str]) -> Model:
    return api.add_model(
        "ContentReviewArtistReviewRequestModel",
        content_type="application/json",
        model_name="ContentReviewArtistReviewRequestModel",
        schema=JsonSchema(
            schema=JsonSchemaVersion.DRAFT4,
            title="ArtistReviewRequest",
            type=JsonSchemaType.OBJECT,
            properties={
                "artistId": JsonSchema(type=JsonSchemaType.STRING),
                "reviewType": JsonSchema(
                    type=JsonSchemaType.STRING,
                    enum=review_types
                ),
            },
            required=["artistId", "reviewType"]
        )
    )

def create_song_review_request_model(api: RestApi, review_types:[str]) -> Model:
    return api.add_model(
        "ContentReviewSongReviewRequestModel",
        content_type="application/json",
        model_name="ContentReviewSongReviewRequestModel",
        schema=JsonSchema(
            schema=JsonSchemaVersion.DRAFT4,
            title="SongReviewRequest",
            type=JsonSchemaType.OBJECT,
            properties={
                "songId": JsonSchema(type=JsonSchemaType.STRING),
                "reviewType": JsonSchema(
                    type=JsonSchemaType.STRING,
                    enum=review_types
                ),
            },
            required=["songId", "reviewType"]
        )
    )
