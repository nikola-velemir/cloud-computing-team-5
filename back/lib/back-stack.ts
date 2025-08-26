import * as cdk from "aws-cdk-lib";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import * as lambda from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class BackStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    const helloLambda = new lambda.Function(this, "helloLambda", {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: "index.handler",
      code: lambda.Code.fromInline(`
        exports.handler = async function(event) {
          return {
            statusCode: 200,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: "Hello from Lambda in eu-central-1!" })
          };
        };
      `),
    });
    const api = new apigateway.RestApi(this, "MyApi", {
      restApiName: "My Service",
      description: "Example API deployed in eu-central-1.",
      deployOptions: { stageName: "prod" },
    });

    // Integrate Lambda with API Gateway
    const getIntegration = new apigateway.LambdaIntegration(helloLambda);
    api.root.addMethod("GET", getIntegration); // GET /

    new cdk.CfnOutput(this, "ApiUrl", {
      value: api.url ?? "Something went wrong",
    });
  }
}
