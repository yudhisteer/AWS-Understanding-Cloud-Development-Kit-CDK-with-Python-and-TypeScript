#!/usr/bin/env python3
import os

import aws_cdk as cdk

from py_starter.py_starter_stack import PyStarterStack
from py_starter.py_handler_stack import PyHandlerStack


app = cdk.App()
# we make a reference to the starter stack so we can use it in the handler stack
starter_stack = PyStarterStack(scope=app, construct_id="PyStarterStack")

handler_stack = PyHandlerStack(scope=app, construct_id="PyHandlerStack",
    # we pass the bucket reference to the handler stack
    bucket=starter_stack.get_bucket
    )

app.synth()
