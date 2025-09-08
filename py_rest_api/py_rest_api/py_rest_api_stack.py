from aws_cdk import (
    # Duration,
    Stack,
    aws_apigateway,
    aws_lambda,
    aws_dynamodb,
)
from constructs import Construct

class PyRestApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        """
        Create a DynamoDB table
        """
        table = aws_dynamodb.TableV2(
            scope=self, 
            id="PyDynamoDBTable",
            partition_key=aws_dynamodb.Attribute(name="id", type=aws_dynamodb.AttributeType.STRING),
            billing=aws_dynamodb.Billing.on_demand(),
        )

        """
        Add CORS to the API Gateway
        # so tha twe can also make request from web-browser
        """
        cors_options = aws_apigateway.CorsOptions(
            allow_origins=aws_apigateway.Cors.ALL_ORIGINS,
            allow_methods=aws_apigateway.Cors.ALL_METHODS,
            allow_headers=aws_apigateway.Cors.DEFAULT_HEADERS,
        )


        """
        Create an API Gateway
        """
        # create an api gateway
        api = aws_apigateway.RestApi(scope=self, id="PyRestApi")
        # create a resource
        resource = api.root.add_resource(
            path_part="employees",
            default_cors_preflight_options=cors_options, # add CORS to the resource
            )

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
            environment={
                "TABLE_NAME": table.table_name
            } # pass the table name to the lambda function
        )

        # allow lambda to read-write to the table
        table.grant_read_write_data(lambda_function)


        """
        Connect the lambda function to the api gateway
        """
        integration = aws_apigateway.LambdaIntegration(lambda_function)
        resource.add_method(http_method="GET", integration=integration)
        resource.add_method(http_method="POST", integration=integration)
        