from aws_cdk import (
    Stack,
    aws_lambda,
    aws_s3,
)
from constructs import Construct

class PySimpleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create some lambda function that we can test
        some_lambda = aws_lambda.Function(
            scope=self,
            id="SomeLambda",
            runtime=aws_lambda.Runtime.PYTHON_3_10,
            code=aws_lambda.Code.from_inline("def handler(event, context): return 'Hello, World!'"),
            handler="index.handler",
        )

        # create some bucket that we can test
        some_bucket = aws_s3.Bucket(self, id="SomeBucket", versioned=True)

        # allow the lambda function to read from the bucket
        some_bucket.grant_read(some_lambda)