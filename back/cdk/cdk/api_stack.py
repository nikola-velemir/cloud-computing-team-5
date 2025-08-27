from aws_cdk import Stack, Fn, CfnOutput, PhysicalName
from aws_cdk.aws_apigateway import RestApi, LambdaIntegration
from aws_cdk.aws_iam import ServicePrincipal, Role
from aws_cdk.aws_lambda import Code, Runtime, Function
from constructs import Construct


class ApiStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.api = RestApi(self, "SongifyApi",rest_api_name="SongifyApi",binary_media_types=["multipart/form-data"])


        hello_lambda = Function(
            self,
            "HelloLambda",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/hello")
        )

        hello = self.api.root.add_resource("hello")
        hello.add_method("GET", LambdaIntegration(hello_lambda))

