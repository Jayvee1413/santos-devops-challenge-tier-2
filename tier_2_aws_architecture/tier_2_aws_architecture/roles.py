from aws_cdk import aws_iam as iam
from policies import generate_pipeline_policy, generate_codebuild_policy, generate_ecs_task_policy, \
    generate_ecs_execution_policy


def generate_pipeline_service_role(scope):
    role = iam.Role(scope=scope,
                    id="JVSANTOSTier2PipelineServiceRole",
                    assumed_by=iam.CompositePrincipal(
                        iam.ServicePrincipal("codepipeline.amazonaws.com"),
                        iam.ServicePrincipal("codebuild.amazonaws.com")),
                    role_name="JVSANTOSTier2PipelineServiceRole")

    role.attach_inline_policy(generate_pipeline_policy(scope))
    return role


def generate_codebuild_role(scope, db_secret_arn):
    role = iam.Role(scope=scope,
                    id="JVSANTOSTier2CodebuildServiceRole",
                    assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
                    role_name="JVSANTOSTier2CodebuildServiceRole")

    role.attach_inline_policy(generate_codebuild_policy(scope, db_secret_arn=db_secret_arn))
    return role


def generate_ecs_task_role(scope):
    role = iam.Role(scope=scope,
                    id="JVSANTOSTier2ECSTaskRole",
                    assumed_by=iam.CompositePrincipal(
                        iam.ServicePrincipal("ec2.amazonaws.com"),
                        iam.ServicePrincipal("ecs-tasks.amazonaws.com")
                    ),
                    role_name="JVSANTOSTier2ECSTaskRole")

    role.attach_inline_policy(generate_ecs_task_policy(scope))
    return role


def generate_ecs_execution_role(scope):
    role = iam.Role(scope=scope,
                    id="JVSANTOSTier2ECSExecutionRole",
                    assumed_by=iam.CompositePrincipal(
                        iam.ServicePrincipal("ec2.amazonaws.com"),
                        iam.ServicePrincipal("ecs-tasks.amazonaws.com")
                    ),
                    role_name="JVSANTOSTier2ECSExecutionRole")

    role.attach_inline_policy(generate_ecs_execution_policy(scope))
    return role