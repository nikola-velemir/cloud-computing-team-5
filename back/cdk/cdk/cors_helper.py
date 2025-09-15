from aws_cdk import aws_apigateway
from aws_cdk.aws_apigateway import MockIntegration


def add_cors_options(api_resource):
    api_resource.add_method(
        "OPTIONS",
        MockIntegration(
            integration_responses=[{
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Headers': "'*'",
                    'method.response.header.Access-Control-Allow-Origin': "'*'",
                    'method.response.header.Access-Control-Allow-Methods': "'GET,POST,PUT,DELETE,OPTIONS'"
                }
            }],
            passthrough_behavior=aws_apigateway.PassthroughBehavior.NEVER,
            request_templates={"application/json": '{"statusCode": 200}'}
        ),
        method_responses=[{
            'statusCode': '200',
            'responseParameters': {
                'method.response.header.Access-Control-Allow-Headers': True,
                'method.response.header.Access-Control-Allow-Origin': True,
                'method.response.header.Access-Control-Allow-Methods': True,
            }
        }]
    )