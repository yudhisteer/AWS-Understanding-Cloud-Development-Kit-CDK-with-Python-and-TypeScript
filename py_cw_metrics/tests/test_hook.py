from hook import handler

# Example SNS event payload to simulate an incoming message for local testing
event = {
    "Records": [
        {
            "Sns": {
                "Message": "Hello, World!"
            }
        }
    ]
}

# Call the handler function with the test event and an empty context
handler(event, {})