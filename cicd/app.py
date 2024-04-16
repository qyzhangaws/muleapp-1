#!/usr/bin/env python3

import aws_cdk as cdk

from cicd.cicd_stack import CicdStack


app = cdk.App()
CicdStack(app, "CicdStack")

app.synth()
