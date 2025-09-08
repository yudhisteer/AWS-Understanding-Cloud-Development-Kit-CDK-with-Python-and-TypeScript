from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    Duration,
)
from constructs import Construct

class PyStarterStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create a bycket - L2 construct
        s3.Bucket(
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