import aws_cdk as core
import aws_cdk.assertions as assertions

from py_testing.py_testing_stack import PySimpleStack


def test_lambda_props():
    # Create a CDK app instance for testing
    app = core.App()
    
    # Instantiate the stack we want to test
    stack = PySimpleStack(app, "py-testing")
    
    # Generate a CloudFormation template from the stack for assertions
    template = assertions.Template.from_stack(stack)

    # Assert that the lambda function has the correct properties
    template.has_resource_properties(
        type="AWS::Lambda::Function", 
        props={
            "Handler": "index.handler",
            "Runtime": "python3.10",
        }
    )

    # Assert that the bucket has the correct properties
    template.has_resource_properties(
        type="AWS::S3::Bucket", 
        props={
        "VersioningConfiguration": {
            "Status": "Enabled",
        },
    })
