import logging
import os
import boto3
import json
import uuid


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize the DynamoDB client outside the handler function
# Get the table name from environment variables passed by CDK
table_name = os.environ.get("TABLE_NAME") 

# Create a DynamoDB resource object to interact with DynamoDB service
dynamodb = boto3.resource("dynamodb")

# Create a table object reference using the table name from environment
table = dynamodb.Table(table_name) 

def handler(event, context):
    logger.info(f"Event: {event}")
    logger.info(f"Context: {context}")

    # Extract the HTTP method from the API Gateway event
    method = event.get("httpMethod")
    if not method:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid request - missing httpMethod"}),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*"
            }
        }

    # Handle GET requests to retrieve an employee by ID
    if method == "GET":
        # Extract the employee ID from the query string parameters
        employee_id = event["queryStringParameters"]["id"]
        logger.info(f"Employee ID: {employee_id}")
        
        # Query DynamoDB table for the employee with the given ID
        response = table.get_item(Key={"id": employee_id})
        
        # Check if the employee was found in the database
        if "Item" in response:
            # Return the employee data with 200 OK status
            return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": "Employee found successfully",
                        "data": response["Item"]
                    }, default=str),
                    "headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "*",
                        "Access-Control-Allow-Headers": "*"
                    }
                }
        else:
            # Return 404 Not Found if employee doesn't exist
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Employee not found"}),
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "*",
                    "Access-Control-Allow-Headers": "*"
                }
            }

    # Handle POST requests to create a new employee
    if method == "POST":
        # Parse the JSON body from the request to get employee data
        item = json.loads(event["body"])
        logger.info(f"Item: {item}")
        
        # Generate a unique ID for the new employee
        item["id"] = str(uuid.uuid4())
        
        # Save the new employee to DynamoDB table
        table.put_item(Item=item)
        
        # Return 201 Created status with the new employee ID
        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Employee created successfully", 
                "data": {"id": item["id"]}
            }),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*"
            }
        }
