from constructs import Construct
from aws_cdk import Stack, aws_lambda as _lambda


class UtilStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.utils_layer = _lambda.LayerVersion(
            self, "UtilsLayer",
            code=_lambda.Code.from_asset("layers/util-layer"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9, _lambda.Runtime.PYTHON_3_10, _lambda.Runtime.PYTHON_3_11],
            description="Lambda Layer sa utils/auth i utils/exception"
        )

        self.requests_layer = _lambda.LayerVersion(
            self, "ApiLayer",
            code=_lambda.Code.from_asset("layers/api-layer"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9, _lambda.Runtime.PYTHON_3_10, _lambda.Runtime.PYTHON_3_11],
            description="Lambda layer with api library"
        )