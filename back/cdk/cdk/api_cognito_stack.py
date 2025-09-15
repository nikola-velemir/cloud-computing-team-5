
from aws_cdk import Stack, RemovalPolicy, aws_cognito as cognito, CfnOutput
from aws_cdk.aws_cognito import AuthFlow, UserPoolGroup, UserPoolOperation
from aws_cdk.aws_lambda import Runtime, Code, Function
from aws_cdk.aws_iam import Policy, Role, ServicePrincipal, PolicyStatement, ManagedPolicy
from constructs import Construct


class ApiCognitoStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.user_pool = cognito.UserPool(
            self, "SongifyUserPool",
            self_sign_up_enabled=True,
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            sign_in_aliases=cognito.SignInAliases(email=True),
            removal_policy=RemovalPolicy.DESTROY
        )

        self.app_client = cognito.UserPoolClient(
            self, "SongifyAppClient",
            user_pool=self.user_pool,
            generate_secret=False,
            auth_flows=AuthFlow(user_password=True)
        )
        user_group = UserPoolGroup(
            self,
            "AuthenticatedUserGroup",
            user_pool=self.user_pool,
            group_name="AuthenticatedUser",
            description="Standard user group"
        )

        admin_group = UserPoolGroup(
            self,
            "AdminGroup",
            user_pool=self.user_pool,
            group_name="Admin",
            description="Administrator group"
        )

        post_confirm_lambda = Function(
            self,
            "PostConfirmationLambda",
            runtime=Runtime.PYTHON_3_11,
            handler="lambda.lambda_handler",
            code=Code.from_asset("src/feature/auth/pre-signup"),
            environment={
                "GROUP_NAME": "AuthenticatedUser"
            }
        )

        post_confirm_lambda.role.add_managed_policy(
            ManagedPolicy.from_aws_managed_policy_name("AmazonCognitoPowerUser")
        )

        self.user_pool.add_trigger(
            UserPoolOperation.POST_CONFIRMATION,
            post_confirm_lambda
        )


        CfnOutput(self, "UserPoolId", value=self.user_pool.user_pool_id)
        CfnOutput(self, "UserPoolClientId", value=self.app_client.user_pool_client_id)