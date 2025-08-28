import os
from dataclasses import asdict
import json
from model.artist import ArtistResponse


TABLE_NAME = os.environ['DYNAMO']
def lambda_handler(event, context):
    performers = [
        ArtistResponse(id='b189c862-0012-4eae-81ea-e6d0dcb33812', name="Boris"),
        ArtistResponse(id='993c58ce-40d2-48e3-8f26-cea8c8820095', name="Ranko"),
        ArtistResponse(id='a682af8b-9270-4cb8-b0c4-e13d9936aa9b', name="Tanja")
    ]

    return {
        'statusCode': 200,
        'body': json.dumps([asdict(p) for p in performers]),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    }
