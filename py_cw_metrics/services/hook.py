import urllib3
import json

# Create a connection pool manager for HTTP requests
http = urllib3.PoolManager()


def handler(event, context):
    """
    AWS Lambda handler function that processes SNS events and sends notifications to Slack.
    
    Args:
        event: AWS Lambda event object containing SNS message data
        context: AWS Lambda context object with runtime information
        
    Returns:
        dict: Response object with status code, message, and HTTP response data
    """
    print("Calling slack...")
    
    # Slack webhook URL - should be configured as environment variable in production
    url = "https://hooks.slack.com/services/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"
    
    # Construct the Slack message payload
    msg = {
        "channel": "#aws-events",  # Target Slack channel
        "text": event['Records'][0]['Sns']['Message']  # Extract SNS message content
    }

    # Encode the message as JSON and convert to bytes for HTTP request
    encoded_msg = json.dumps(msg).encode("utf-8")
    
    # Send POST request to Slack webhook URL
    resp = http.request(method="POST", url=url, body=encoded_msg)

    # Return response object with status and message details
    print({
        "statusCode": resp.status,
        "message": event['Records'][0]['Sns']['Message'],
        "response": resp.data,
    })