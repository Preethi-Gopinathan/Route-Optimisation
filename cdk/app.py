#!/usr/bin/env python3
import aws_cdk as cdk
from flask_ebs_stack import FlaskEbsStack

app = cdk.App()
FlaskEbsStack(app, "FlaskEbsStack")
app.synth()
