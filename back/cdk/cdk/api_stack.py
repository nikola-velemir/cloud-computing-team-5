from aws_cdk import Stack, aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigw
from aws_cdk.aws_iam import PolicyStatement
from aws_cdk.aws_lambda import Code, Runtime, Function
from cdk.cors_helper import add_cors_options
from constructs import Construct

CLIENT_ID = "2bhb4d2keh19gbj25tuild6ti1"

class ApiStack(Stack):
    def __init__(self, scope: Construct, id: str, user_pool, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.api = apigw.RestApi(self, "SongifyApi", rest_api_name="SongifyApi", binary_media_types=["multipart/form-data"])

        register_lambda = Function(
            self,
            "RegisterLambda",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/auth/register"),
            environment={
                "USER_POOL_ID": user_pool.user_pool_id,
                "CLIENT_ID": CLIENT_ID
            }
        )
        register_lambda.add_to_role_policy(
            PolicyStatement(
                actions=[
                    "cognito-idp:AdminCreateUser",
                    "cognito-idp:AdminConfirmSignUp",
                    "cognito-idp:AdminAddUserToGroup"
                ],
                resources=[user_pool.user_pool_arn]
            )
        )
        requests_layer = _lambda.LayerVersion(
            self, "ApiLayer",
            code=_lambda.Code.from_asset("layers/api-layer"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9, _lambda.Runtime.PYTHON_3_10],
            description="Lambda layer with api library"
        )


        login_lambda = _lambda.Function(
            self,
            "LoginLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/auth/login"),
            environment={
                "CLIENT_ID": CLIENT_ID
            },
            layers=[requests_layer]

        )

        logout_lambda = Function(
            self,
            "LogoutLambda",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/auth/logout")
        )
        hello_lambda = Function(
            self,
            "HelloLambda",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/hello_authorize")
        )

        # Cognito Authorizer
        authorizer = apigw.CognitoUserPoolsAuthorizer(
            self, "CognitoAuthorizer",
            cognito_user_pools=[user_pool]
        )

        # Resource i metoda
        hello = self.api.root.add_resource("hello_authorize")
        hello.add_method(
            "GET",
            apigw.LambdaIntegration(hello_lambda),
            authorizer=authorizer
        )
        auth = self.api.root.add_resource("auth")

        register = auth.add_resource("register")
        register.add_method("POST",apigw.LambdaIntegration(register_lambda), authorizer=None)

        login = auth.add_resource("login")
        login.add_method("POST", apigw.LambdaIntegration(login_lambda), authorizer=None)

        logout = auth.add_resource("logout")
        logout.add_method("POST", apigw.LambdaIntegration(logout_lambda))

        add_cors_options(hello)
        add_cors_options(logout)
        add_cors_options(login)
        add_cors_options(register)
