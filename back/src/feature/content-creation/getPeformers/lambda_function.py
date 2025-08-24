from dataclasses import asdict
import json
from songify_config.headers import HEADERS
from model.peformer import PerformerResponse
def lambda_handler(event,context):

    performers = [
        PerformerResponse(id='b189c862-0012-4eae-81ea-e6d0dcb33812',name="Boris"),
        PerformerResponse(id='993c58ce-40d2-48e3-8f26-cea8c8820095',name="Ranko"),
        PerformerResponse(id='a682af8b-9270-4cb8-b0c4-e13d9936aa9b',name="Tanja")
    ]

    return {
        'statusCode':200,
        'body': json.dumps( [asdict(p) for p in performers]),
        'headers':HEADERS
    }