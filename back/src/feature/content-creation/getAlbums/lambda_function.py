from dataclasses import asdict
import json
import boto3
from model.album import AlbumResponse
from songify_config.headers import HEADERS

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("SongifyDynamo")

def lambda_handler(event,context):
    db_response = table.scan(
        FilterExpression = "begins_with(PK, :album)",
        ExpressionAttributeValues = {
            ":album":"ALBUM#"
        }
    )

    items = db_response.get("Items",[])

    responses = [asdict(AlbumResponse(
        id= item['PK'].split('#')[1],
        title= item.get("Title",""),
        year= int(item.get("CreatedAt").split('-')[2])
        )) for item in items]
    
    return {
        'statusCode':200,
        'body': json.dumps(responses),
        'headers':HEADERS
    }