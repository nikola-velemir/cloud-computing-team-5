import os
from dataclasses import asdict
import json
import boto3
from model.album import AlbumResponse

TABLE_NAME = os.environ['DYNAMO']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)
def lambda_handler(event, context):
    try:
        db_response = table.scan(
            FilterExpression="begins_with(PK, :album)",
            ExpressionAttributeValues={
                ":album": "ALBUM#"
            }
        )

        items = db_response.get("Items", [])

        responses = [asdict(AlbumResponse(
            id=item['PK'].split('#')[1],
            title=item.get("Title", ""),
            year=int(item.get("ReleaseDate", "0000-00-00").split('-')[2]),
            artistIds=item.get("ArtistIds", []),
        )) for item in items]

        return {
            'statusCode': 200,
            'body': json.dumps(responses),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
