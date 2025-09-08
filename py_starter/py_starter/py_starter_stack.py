from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    Duration,
    CfnOutput,
    CfnCondition,
    Fn, 
)
from constructs import Construct

class PyStarterStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create a bycket - L2 construct
        my_bucket = s3.Bucket(
            self, 
            id="PyStarterBucket", 
            bucket_name="py-starter-bucket",
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="PyStarterLifecycleRule",
                    expiration=Duration.days(1), # lifecycle rule to delete the bucket after 1 day
                )
            ]
            )

        # we cannot print the bucket name like this because we can even genrate this template without internet
        # the bucket name is avaiulable once created by CloudFormation
        print("My bucket name is: ", my_bucket.bucket_name) # will print the cdk token - ${Token[TOKEN.24]}


        CfnOutput(
            self,
            id="PyStarterBucketNameOutput", 
            value=my_bucket.bucket_name,

            # condition to export the bucket name
            # both lhs and rhs must be true to export the bucket name
            condition=CfnCondition(
                self,
                "PyStarterBucketNameOutputCondition",
                expression=Fn.condition_equals(lhs=True, rhs=True)
            ),

            description="The name of the bucket", 
            export_name="PyStarterBucketNameOutputExport", # export name of the output so we can use it in other stacks
        )

        # example of output from CfnOutput:
        """
        Outputs:
        PyStarterStack.PyStarterBucketNameOutput = py-starter-bucket
        Stack ARN:
        arn:aws:cloudformation:us-east-1:503561429929:stack/PyStarterStack/196b7370-8c50-11f0-93ab-0ecdb2169a8f
        """
