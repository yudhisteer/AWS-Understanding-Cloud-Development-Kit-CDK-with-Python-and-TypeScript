from aws_cdk import (
    Stack,
    aws_s3,
    aws_cloudfront,
    aws_cloudfront_origins,
    aws_s3_deployment,
    CfnOutput,
)
import os

from constructs import Construct

class PyWebStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an S3 bucket to store the web application files
        # This bucket will serve as the origin for our CloudFront distribution
        deployment_bucket = aws_s3.Bucket(
            scope=self,
            id="PyWebDeploymentBucket",
        )
        
        # Define the path to the built web application files
        # The dist directory should contain the compiled/built frontend assets
        ui_dir = os.path.join(os.path.dirname(__file__), "..", "..", "web", "dist")
        if not os.path.exists(ui_dir):
            raise FileNotFoundError(f"Do 'npm run build' if dist dir not in this directory: {ui_dir}")
        
        # Create an Origin Access Identity (OAI) for CloudFront
        # This allows CloudFront to securely access the S3 bucket without making it publicly readable
        origin_identity = aws_cloudfront.OriginAccessIdentity(
            scope=self,
            id="PyWebOriginIdentity",
        )
        
        # Grant the Origin Access Identity read permissions to the S3 bucket
        # This ensures CloudFront can fetch files from the bucket
        deployment_bucket.grant_read(origin_identity)
        
        # Create a CloudFront distribution to serve the web application globally
        # This provides caching, SSL termination, and global edge locations for better performance
        cloudfront_distribution = aws_cloudfront.Distribution(
            scope=self,
            id="PyWebDistribution",
            default_root_object="index.html",  # Serve index.html for root requests
            default_behavior=aws_cloudfront.BehaviorOptions(
                origin=aws_cloudfront_origins.S3Origin(
                    bucket=deployment_bucket,
                    origin_access_identity=origin_identity,
                ),
            ),
        )

        # Deploy the web application files to the S3 bucket
        # This automatically uploads files from the local dist directory to S3
        # and invalidates the CloudFront cache when files change
        # When we invalidate a file, CloudFront removes it from cache so the next request 
        # will fetch the fresh/updated version from the S3 bucket instead of serving the old cached version.
        aws_s3_deployment.BucketDeployment(
            scope=self,
            id="PyWebDeployment",
            sources=[aws_s3_deployment.Source.asset(ui_dir)],
            destination_bucket=deployment_bucket,
            distribution=cloudfront_distribution,
        )
        
        # Output the CloudFront distribution domain name
        # This URL can be used to access the deployed web application
        CfnOutput(
            scope=self,
            id="PyWebDistributionDomainName",
            value=cloudfront_distribution.distribution_domain_name,
            description="The domain name of the CloudFront distribution",
            export_name="PyWebDistributionDomainName",
        )