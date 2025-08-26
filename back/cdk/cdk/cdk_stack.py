import os
from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        hello_lambda = _lambda.Function(
            self,
            "HelloLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler= "hello.handler",
            code=_lambda.Code.from_asset(os.path.join(os.getcwd(), "src")),
        )

        api =apigw.RestApi(
            self, "SongifyApi",
            rest_api_name="SongifyApi",
            description="This service serves song-related information."
        )
        hello = api.root.add_resource('hello')
        hello.add_method("GET",apigw.LambdaIntegration(hello_lambda))

        self.api_url = api.url
