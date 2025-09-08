from aws_cdk import (
    # Duration,
    Stack,
    aws_apigateway,
    aws_lambda,
)
from constructs import Construct

class PyRestApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        """
        Create a simple API Gateway with a GET method
        """
        # create an api gateway
        api = aws_apigateway.RestApi(scope=self, id="PyRestApi")
        # create a resource
        resource = api.root.add_resource(path_part="hello")
        

        """
        Create a lambda function
        """
        # create a lambda function
        lambda_function = aws_lambda.Function(
            scope=self, 
            id="PyLambdaFunction",
            runtime=aws_lambda.Runtime.PYTHON_3_10,
            code=aws_lambda.Code.from_asset("services"), # go to services dir
            handler="index.handler", # in services dir, get index.py file and get the handler function
        )


        """
        Connect the lambda function to the api gateway
        """
        integration = aws_apigateway.LambdaIntegration(lambda_function)
        resource.add_method(http_method="GET", integration=integration)
        resource.add_method(http_method="POST", integration=integration)
        