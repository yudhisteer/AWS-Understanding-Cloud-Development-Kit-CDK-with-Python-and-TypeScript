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

        suffix = self.__initialize_suffix()

        # create a bucket - L2 construct
        # self: construct belongs to this stack
        # bucket belongs to this stack when using self.my_bucket.bucket_name
        self.my_bucket = s3.Bucket(
            self, 
            id="MyS3Bucket",  # construct ID
            bucket_name=f"py-starter-bucket-02-{suffix}", 
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="PyStarterLifecycleRule",
                    expiration=Duration.days(1), # lifecycle rule to delete the bucket after 1 day
                )
            ]
            )

        # we cannot print the bucket name like this because we can even genrate this template without internet
        # the bucket name is avaiulable once created by CloudFormation
        print("My bucket name is: ", self.my_bucket.bucket_name) # will print the cdk token - ${Token[TOKEN.24]}


        CfnOutput(
            self,
            id="PyStarterBucketNameOutput", 
            value=self.my_bucket.bucket_name,

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

    def __initialize_suffix(self):
        print("Original stack ID: ", self.stack_id)
        short_stack_id = Fn.select(2, Fn.split("/", self.stack_id))
        print("Short stack ID: ", short_stack_id)
        suffix = Fn.select(4, Fn.split("-", short_stack_id))
        print("Suffix: ", suffix)
        return suffix

    @property
    def get_bucket(self):
        return self.my_bucket