import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.hook import handler

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