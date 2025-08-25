import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { DynamoDBClient, PutItemCommand } from "@aws-sdk/client-dynamodb";
import multipart from "lambda-multipart-parser";
import { v4 as uuidv4 } from "uuid";

const BUCKET_NAME = "albums-bucket-cc5-2025";
const s3 = new S3Client({});
const dynamodb = new DynamoDBClient({});

const HEADERS = {
  "Content-Type": "application/json",
  "Access-Control-Allow-Origin": "*",
};

export const handler = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  if (!event.headers["content-type"] && !event.headers["Content-Type"]) {
    return {
      statusCode: 400,
      body: JSON.stringify({ message: "No Content-Type header" }),
      headers: HEADERS,
    };
  }

  try {
    const parsed = await multipart.parse(event);

    const albumName = parsed["albumName"];
    const artistIds = parsed["artistIds"]
      ? JSON.parse(parsed["artistIds"])
      : [];
    const releaseDate = parsed["releaseDate"] || "";
    const file = parsed.files.find((f) => f.fieldname === "albumImage");

    if (!albumName || !artistIds.length) {
      return {
        statusCode: 400,
        body: JSON.stringify({ message: "Missing albumName or artistIds" }),
        headers: HEADERS,
      };
    }

    const albumId = uuidv4();
    let imageUrl: string | null = null;

    if (file) {
      const imageKey = `albums/${albumId}/cover/cover.jpg`;
      await s3.send(
        new PutObjectCommand({
          Bucket: BUCKET_NAME,
          Key: imageKey,
          Body: file.content,
          ContentType: file.contentType || "image/jpeg",
        })
      );
      imageUrl = `https://${BUCKET_NAME}.s3.amazonaws.com/${imageKey}`;
    }

    await dynamodb.send(
      new PutItemCommand({
        TableName: "SongifyDynamo",
        Item: {
          PK: { S: `ALBUM#${albumId}` },
          SK: { S: "METADATA" },
          Title: { S: albumName },
          ArtistIds: { L: artistIds.map((id: string) => ({ S: id })) },
          ImageUrl: { S: imageUrl || "" },
          ReleaseDate: { S: releaseDate },
        },
      })
    );

    return {
      statusCode: 201,
      body: JSON.stringify({ albumId, imageUrl }),
      headers: HEADERS,
    };
  } catch (err) {
    console.error(err);
    return {
      statusCode: 500,
      body: JSON.stringify({ message: "Internal Server Error", error: err }),
      headers: HEADERS,
    };
  }
};
