#!/usr/bin/env python3
import os

from aws_cdk import core

from tier_2_aws_architecture.tier_2_aws_architecture_stack import Tier2VPCAwsArchitectureStack, \
    Tier2ECSAwsArchitectureStack, Tier2CICDAwsArchitectureStack, Tier2CDNAwsArchitectureStack

app = core.App()
account_number = os.getenv("CDK_DEFAULT_ACCOUNT")
region = os.getenv("CDK_DEFAULT_REGION")

vpc_stack = Tier2VPCAwsArchitectureStack(app, "JVSANTOSTier2AwsArchitectureStack",
                                         env=core.Environment(account=account_number, region=region))

ecs_stack = Tier2ECSAwsArchitectureStack(app, "JVSANTOSTier2ECSAwsArchitectureStack", vpc_stack,
                                         env=core.Environment(account=account_number, region=region))

cicd_stack = Tier2CICDAwsArchitectureStack(app, "JVSANTOSTier2CICDAwsArchitectureStack", vpc_stack, ecs_stack,
                                           env=core.Environment(account=account_number, region=region))

cdn_stack = Tier2CDNAwsArchitectureStack(app, "JVSANTOSTier2CDNAwsArchitectureStack", ecs_stack,
                                           env=core.Environment(account=account_number, region=region))

app.synth()
