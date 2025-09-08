from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    Duration,
    CfnOutput,
    CfnCondition,
    Fn, 
    aws_lambda
)
from constructs import Construct

class PyHandlerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, bucket: s3.Bucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        aws_lambda.Function(self,
            id="MyLambdaFunction",
            handler="index.handler",
            runtime=aws_lambda.Runtime.PYTHON_3_10,
            code=aws_lambda.Code.from_inline(
                "import os\ndef handler(event, context): return {'message': 'Hello, World!', 'bucket_arn': os.environ['BUCKET_ARN']}"
                ),
            environment={
                "BUCKET_ARN": bucket.bucket_arn
            }
        )
