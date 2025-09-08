"""
This is the handler for the lambda function
"""

import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(f"Event: {event}")
    logger.info(f"Context: {context}")
    return {
        "statusCode": 200,
        "body": "Hello, World!"
    }
