import { APIGatewayProxyHandler } from "aws-lambda";
import { Performer } from "./model/Performer";
import { headers } from "./headers/headers";

export const handler: APIGatewayProxyHandler = async (event) => {
  const genres: Performer[] = [
    { id: "550e8400-e29b-41d4-a716-446655440000", name: "Action" },
    { id: "550e8400-e29b-41d4-a716-446655440001", name: "Adventure" },
    { id: "550e8400-e29b-41d4-a716-446655440002", name: "Comedy" },
    { id: "550e8400-e29b-41d4-a716-446655440003", name: "Drama" },
    { id: "550e8400-e29b-41d4-a716-446655440004", name: "Horror" },
    { id: "550e8400-e29b-41d4-a716-446655440005", name: "Western" },
  ];

  return {
    statusCode: 200,
    headers: headers,
    body: JSON.stringify(genres),
  };
};
