import os
from aws_cdk import Stack, RemovalPolicy
import aws_cdk.aws_cloudfront as cloudfront
import aws_cdk.aws_cloudfront_origins as cforigins
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_s3_deployment as s3_deployment
from constructs import Construct

class FrontAppDeploymentStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # 1. Private S3 bucket
        deployment_bucket = s3.Bucket(
            self,
            "FrontAppDeploymentBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # Private bucket
        )

        # 2. CloudFront distribution with secure access to bucket
        distribution = cloudfront.Distribution(
            self,
            "FrontAppDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=cforigins.S3Origin(deployment_bucket),  # automatically sets OAC
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            ),
            default_root_object="index.html",
        )

        # 3. Deploy Angular build to S3 and invalidate CloudFront cache
        angular_build_path = os.path.join(os.getcwd(), "../../front-app/dist/front-app/browser")
        s3_deployment.BucketDeployment(
            self,
            "DeployFrontApp",
            sources=[s3_deployment.Source.asset(angular_build_path)],
            destination_bucket=deployment_bucket,
            distribution=distribution,
            distribution_paths=["/*"]
        )
