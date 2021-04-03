from aws_cdk import aws_ec2 as ec2


def generate_vpc(scope):
    vpc = ec2.Vpc(
        scope=scope,
        id="Tier2VPC",
        cidr="10.0.0.0/16",
        subnet_configuration=[
            ec2.SubnetConfiguration(
                name="Public",
                subnet_type=ec2.SubnetType.PUBLIC,
                cidr_mask=20
            ),
            ec2.SubnetConfiguration(
                name="Isolated",
                subnet_type=ec2.SubnetType.ISOLATED,
                cidr_mask=20
            ),
            ec2.SubnetConfiguration(
                name="Private",
                subnet_type=ec2.SubnetType.PRIVATE,
                cidr_mask=19
            ),
        ],
        enable_dns_hostnames=True,
        max_azs=3,
        enable_dns_support=True,
        nat_gateways=1,
    )

    return vpc
