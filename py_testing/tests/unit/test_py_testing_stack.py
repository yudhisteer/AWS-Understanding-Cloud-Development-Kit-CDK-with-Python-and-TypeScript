import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest

from py_testing.py_testing_stack import PySimpleStack
from aws_cdk.assertions import Match, Capture

# we can create a simple template function to reuse the template for the tests
# Extract the template creation into a pytest fixture to avoid code duplication
# across multiple test functions. This fixture creates the CDK stack once per
# test session and reuses the same template for all tests, improving performance
# and ensuring consistency across tests.
@pytest.fixture(scope="session")
def simple_template():
    # Create a CDK app and stack instance
    app = core.App()
    stack = PySimpleStack(app, "py-testing")
    # Generate the CloudFormation template from the stack for testing
    template = assertions.Template.from_stack(stack)
    return template


def test_lambda_props(simple_template):

    # Assert that the lambda function has the correct properties
    simple_template.has_resource_properties(
        type="AWS::Lambda::Function", 
        props={
            "Handler": "index.handler",
            "Runtime": "python3.10",
        }
    )

    # Assert that the bucket has the correct properties
    simple_template.has_resource_properties(
        type="AWS::S3::Bucket", 
        props={
        "VersioningConfiguration": {
            "Status": "Enabled",
        },
    })

    # make sure we have only one lambda function
    simple_template.resource_count_is(type="AWS::Lambda::Function", count=1)


def test_lambda_runtime_with_matcher(simple_template):
    """Test that demonstrates using regex matchers to validate Lambda runtime."""
    
    # Use a string pattern matcher to validate that the Lambda function's runtime
    # matches the expected Python version pattern (e.g., python3.10, python3.11, etc.)
    # This is more flexible than exact string matching and allows for runtime version updates
    simple_template.has_resource_properties(
        type="AWS::Lambda::Function", 
        props={
            "Runtime": Match.string_like_regexp("python3.*"), # Match any Python 3.x runtime version
        }
    )


def test_lambda_bucket_with_matcher(simple_template):
    """Test that validates IAM policy permissions between Lambda and S3 bucket using matchers."""
    
    # Verify that an IAM policy exists that grants the Lambda function read access to the S3 bucket
    # This test uses advanced matchers to check the policy structure without requiring exact matches
    # which makes the test more resilient to changes in policy formatting or additional permissions
    simple_template.has_resource_properties(
        type="AWS::IAM::Policy",
        props=Match.object_like({
            # Check the policy document structure
            "PolicyDocument": {
                "Statement": [
                    {
                        # Verify the policy includes resources that reference our bucket
                        "Resource": [
                            {
                                # Check for CloudFormation function that gets the bucket ARN
                                "Fn::GetAtt": [
                                    Match.string_like_regexp("SomeBucket"), # Match bucket name pattern
                                    "Arn"  # Ensure we're getting the ARN attribute
                                ]
                            },
                            Match.any_value()  # Allow for additional resources in the policy
                        ]
                    }
                ]
            }
        })
    )


def test_lambda_actions_with_captors(simple_template):
    """Test that validates Lambda function actions using capture objects."""
    
    # Use capture objects to verify that the Lambda function has specific actions
    # This approach allows for more flexible assertions about the function's behavior
    # without requiring exact matches in the template
    
    # Create a Capture object to extract the actual IAM actions from the policy
    # This allows us to inspect the values that CDK generates dynamically
    capture = Capture()
    
    # Search for an IAM policy that contains actions and capture those actions
    # The capture object will store whatever value is found in the "Action" field
    simple_template.has_resource_properties(
        type="AWS::IAM::Policy", 
        props={"PolicyDocument": {
            "Statement": [
                {
                    "Action": capture  # Capture the actual actions defined in the policy
                }
            ]
        }
    })

    # Define the expected S3 read permissions that should be granted to the Lambda
    # These are the actions we expect based on our CDK code that calls bucket.grant_read()
    # can be found from py_testing/cdk.out/PyTestingStack.template.json after doing 'cdk synth'
    expected_actions = [
        "s3:GetObject*",   # Allows reading objects from the bucket
        "s3:GetBucket*",   # Allows getting bucket metadata and properties
        "s3:List*"         # Allows listing bucket contents
        ]

    # Verify that the captured actions match our expected permissions exactly
    # We sort both arrays to ensure order doesn't affect the comparison
    assert sorted(capture.as_array()) == sorted(expected_actions)