from aws_cdk import core as cdk, core
from aws_cdk.aws_ec2 import SubnetSelection, SubnetType
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedTaskImageOptions
from aws_cdk.aws_elasticloadbalancingv2 import ListenerAction
from aws_cdk.core import Tags
from buckets import generate_pipeline_bucket
from certificates import generate_acm_certificate
from cloudfront_distributions import generate_cloudfront_distribution
from codebuilds import generate_codebuild_project
from codestar_connections import generate_codestar_connection
from databases import generate_db_secret, generate_db_instance
from hosted_zones import generate_lookedup_hosted_zone, generate_record_in_hosted_zone
from nacls import generate_public_nacl, generate_private_nacl, generate_isolated_nacl
from pipelines import generate_pipeline
from repositories import generate_ecr_repository
from roles import generate_pipeline_service_role, generate_codebuild_role, generate_ecs_task_role, \
    generate_ecs_execution_role
from security_groups import generate_load_balancer_security_group, generate_app_security_group, \
    generate_rds_security_group
from vpcs import generate_vpc

from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_codedeploy as codedeploy
from aws_cdk import aws_elasticloadbalancingv2 as elbv2


class Tier2VPCAwsArchitectureStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC Creation
        self.vpc = generate_vpc(scope=self)

        # NACLs Creation
        generate_public_nacl(scope=self, vpc=self.vpc)
        generate_private_nacl(scope=self, vpc=self.vpc)
        generate_isolated_nacl(scope=self, vpc=self.vpc, private_subnets=self.vpc.private_subnets)

        # Generate CodeStar Connection

        self.codestar_connection = generate_codestar_connection(scope=self)

        # RDS Creation
        # Security Group Creation
        self.load_balancer_security_group = generate_load_balancer_security_group(scope=self, vpc=self.vpc)
        self.app_security_group = generate_app_security_group(scope=self,
                                                              vpc=self.vpc,
                                                              load_balancer_sg=self.load_balancer_security_group)
        self.rds_security_group = generate_rds_security_group(scope=self, vpc=self.vpc)

        # RDS
        self.db_secret = generate_db_secret(scope=self)
        generate_db_instance(scope=self, vpc=self.vpc, security_group=self.rds_security_group, db_secret=self.db_secret)

        # Hosted Zone and ACM Certificate

        self.hosted_zone = generate_lookedup_hosted_zone(scope=self)
        self.acm_certificate = generate_acm_certificate(scope=self, hosted_zone=self.hosted_zone)
        Tags.of(scope).add("Name", "jvsantos.tier2")


class Tier2ECSAwsArchitectureStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, vpc_stack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cluster = ecs.Cluster(
            self, 'fargate-service-autoscaling',
            vpc=vpc_stack.vpc,

        )
        self.vpc_stack = vpc_stack

        task_role = generate_ecs_task_role(scope=self)
        execution_role = generate_ecs_execution_role(scope=self)

        # # Create Fargate Service
        self.fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "JVSantosTier2FargateService",
            cluster=cluster,
            task_image_options=ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                execution_role=execution_role,
                task_role=task_role
            ),
            desired_count=2,
        )
        self.fargate_service.load_balancer.add_listener(
            id="JVSANTOSTier2HTTPSListener",
            certificates=[self.vpc_stack.acm_certificate],
            port=443,
            default_action=ListenerAction.forward([self.fargate_service.target_group])
        )

        # fargate_service.task_definition.default_container.container_name

        self.fargate_service.service.connections.security_groups[0].add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc_stack.vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(80),
            description="Allow http inbound from VPC"
        )

        self.fargate_service.service.connections.security_groups[0].add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc_stack.vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(443),
            description="Allow https inbound from VPC"
        )

        self.fargate_service.service.connections.security_groups[0].add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc_stack.vpc.vpc_cidr_block),
            connection=ec2.Port.tcp_range(start_port=1024, end_port=65535),
            description="Allow ephemeral inbound from VPC"
        )

        scaling = self.fargate_service.service.auto_scale_task_count(
            max_capacity=4,
            min_capacity=2
        )
        scaling.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=50,
            scale_in_cooldown=core.Duration.seconds(60),
            scale_out_cooldown=core.Duration.seconds(60),
        )

        core.CfnOutput(
            self, "JVSANTOSTier2LoadBalancerDNS",
            value=self.fargate_service.load_balancer.load_balancer_dns_name
        )

        Tags.of(scope).add("Name", "jvsantos.tier2")


class Tier2CICDAwsArchitectureStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, vpc_stack, ecs_stack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ecr_repo = generate_ecr_repository(scope=self)

        # Bucket creation
        pipeline_bucket = generate_pipeline_bucket(scope=self)

        # Pipeline Creation
        pipeline_service_role = generate_pipeline_service_role(scope=self)
        codebuild_role = generate_codebuild_role(scope=self, db_secret_arn=vpc_stack.db_secret.secret_full_arn)

        # Codebuild Project Creation
        codebuild_project = generate_codebuild_project(scope=self, db_secret=vpc_stack.db_secret, role=codebuild_role,
                                                       ecr_repo_name=ecr_repo.repository_name)

        pipeline = generate_pipeline(scope=self, bucket=pipeline_bucket, role=pipeline_service_role,
                                     codebuild_project=codebuild_project,
                                     codestar_connection=vpc_stack.codestar_connection,
                                     ecs_service=ecs_stack.fargate_service.service)

        Tags.of(scope).add("Name", "jvsantos.tier2")


class Tier2CDNAwsArchitectureStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, ecs_stack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cloudfront_distribution = generate_cloudfront_distribution(scope=self,
                                                                   certificate=ecs_stack.vpc_stack.acm_certificate,
                                                                   ecs_url=ecs_stack.fargate_service.load_balancer.load_balancer_dns_name)
        record = generate_record_in_hosted_zone(scope=self, hosted_zone=ecs_stack.vpc_stack.hosted_zone,
                                                cloudfront_distribution=cloudfront_distribution)
        core.CfnOutput(
            scope=self, id="JVSantosTier2Domain", value=record.domain_name
        )
        Tags.of(scope).add("Name", "jvsantos.tier2")
