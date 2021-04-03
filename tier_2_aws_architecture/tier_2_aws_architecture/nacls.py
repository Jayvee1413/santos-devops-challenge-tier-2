from typing import List

from aws_cdk import aws_ec2 as ec2


def generate_public_nacl(scope, vpc: ec2.Vpc):
    nacl = ec2.CfnNetworkAcl(
        scope=scope,
        id="public_network_acl",
        vpc_id=vpc.vpc_id,
        tags=[{"key": "Name", "value": "Tier_1_ACL_Public"}],
    )

    generate_public_nacl_entries(scope=scope, public_nacl=nacl)

    # Associate Public subnets to Public NACL
    counter = 0
    for subnet in vpc.public_subnets:
        ec2.CfnSubnetNetworkAclAssociation(
            scope=scope,
            id=f"public_nacl_subnet_assoc_{counter}",
            network_acl_id=nacl.ref,
            subnet_id=subnet.subnet_id,
        )
        counter += 1

    return nacl


def generate_private_nacl(scope, vpc: ec2.Vpc):
    nacl = ec2.CfnNetworkAcl(
        scope=scope,
        id="private_network_acl",
        vpc_id=vpc.vpc_id,
        tags=[{"key": "Name", "value": "Tier_1_ACL_Private"}],
    )

    generate_private_nacl_entries(scope=scope, vpc=vpc, private_nacl=nacl)

    # Associate Public subnets to Public NACL
    counter = 0
    for subnet in vpc.private_subnets:
        ec2.CfnSubnetNetworkAclAssociation(
            scope=scope,
            id=f"private_nacl_subnet_assoc_{counter}",
            network_acl_id=nacl.ref,
            subnet_id=subnet.subnet_id,
        )
        counter += 1

    return nacl


def generate_isolated_nacl(scope, vpc: ec2.Vpc, private_subnets: List[ec2.ISubnet]):
    nacl = ec2.CfnNetworkAcl(
        scope=scope,
        id="isolated_network_acl",
        vpc_id=vpc.vpc_id,
        tags=[{"key": "Name", "value": "Tier_1_ACL_Isolated"}],
    )

    generate_isolated_nacl_entries(scope=scope, isolated_nacl=nacl, private_subnets=private_subnets)

    # Associate Public subnets to Public NACL
    counter = 0
    for subnet in vpc.isolated_subnets:
        ec2.CfnSubnetNetworkAclAssociation(
            scope=scope,
            id=f"isolated_nacl_subnet_assoc_{counter}",
            network_acl_id=nacl.ref,
            subnet_id=subnet.subnet_id,
        )
        counter += 1

    return nacl


def generate_public_nacl_entries(scope, public_nacl):
    # For protocol numbers, check out
    # https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml

    # Inbound Public NACL Entries
    ec2.CfnNetworkAclEntry(
        scope,
        rule_number=200,
        rule_action="ALLOW",
        protocol=6,
        id="public_nacl_http_port_inbound",
        network_acl_id=public_nacl.ref,
        cidr_block="0.0.0.0/0",
        port_range={"from": 80, "to": 80},
        egress=False,
    )

    ec2.CfnNetworkAclEntry(
        scope,
        rule_number=210,
        rule_action="ALLOW",
        protocol=6,
        id="public_nacl_https_port_inbound",
        network_acl_id=public_nacl.ref,
        cidr_block="0.0.0.0/0",
        port_range={"from": 443, "to": 443},
        egress=False,
    )
    ec2.CfnNetworkAclEntry(
        scope,
        rule_number=220,
        rule_action="DENY",
        protocol=6,
        id="public_nacl_ssh_port_inbound",
        network_acl_id=public_nacl.ref,
        cidr_block="0.0.0.0/0",
        port_range={"from": 22, "to": 22},
        egress=False,
    )

    ec2.CfnNetworkAclEntry(
        scope,
        rule_number=230,
        rule_action="ALLOW",
        protocol=6,
        id="public_nacl_ephemeral_port_inbound",
        network_acl_id=public_nacl.ref,
        cidr_block="0.0.0.0/0",
        port_range={"from": 1024, "to": 65535},
        egress=False,
    )

    # Outbound Public NACL Entries
    ec2.CfnNetworkAclEntry(
        scope,
        rule_number=200,
        rule_action="ALLOW",
        protocol=6,
        id="public_nacl_http_port_outbound",
        network_acl_id=public_nacl.ref,
        cidr_block="0.0.0.0/0",
        port_range={"from": 80, "to": 80},
        egress=True,
    )

    ec2.CfnNetworkAclEntry(
        scope,
        rule_number=210,
        rule_action="ALLOW",
        protocol=6,
        id="public_nacl_https_port_outbound",
        network_acl_id=public_nacl.ref,
        cidr_block="0.0.0.0/0",
        port_range={"from": 443, "to": 443},
        egress=True,
    )
    ec2.CfnNetworkAclEntry(
        scope,
        rule_number=220,
        rule_action="ALLOW",
        protocol=6,
        id="public_nacl_ephemeral_port_outbound",
        network_acl_id=public_nacl.ref,
        cidr_block="0.0.0.0/0",
        port_range={"from": 1024, "to": 65535},
        egress=True,
    )

    ec2.CfnNetworkAclEntry(
        scope,
        rule_number=230,
        rule_action="ALLOW",
        protocol=6,
        id="public_nacl_ssh_port_outbound",
        network_acl_id=public_nacl.ref,
        cidr_block="0.0.0.0/0",
        port_range={"from": 22, "to": 22},
        egress=True,
    )


def generate_private_nacl_entries(scope, private_nacl, vpc: ec2.Vpc):
    # For protocol numbers, check out
    # https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
    # Inbound Private NACL Entries

    ec2.CfnNetworkAclEntry(
        scope,
        rule_number=200,
        rule_action="ALLOW",
        protocol=6,
        id="private_nacl_all_port_inbound",
        network_acl_id=private_nacl.ref,
        cidr_block=vpc.vpc_cidr_block,
        port_range={"from": 0, "to": 65535},
        egress=False,
    )

    ec2.CfnNetworkAclEntry(
        scope,
        rule_number=210,
        rule_action="ALLOW",
        protocol=6,
        id="private_nacl_all_port_outside_inbound",
        network_acl_id=private_nacl.ref,
        cidr_block="0.0.0.0/0",
        port_range={"from": 1024, "to": 65535},
        egress=False,
    )

    ec2.CfnNetworkAclEntry(
        scope,
        rule_number=220,
        rule_action="ALLOW",
        protocol=6,
        id="private_nacl_https_port_outside_inbound",
        network_acl_id=private_nacl.ref,
        cidr_block="0.0.0.0/0",
        port_range={"from": 443, "to": 443},
        egress=False,
    )

    # Outbound Private NACL Entries

    ec2.CfnNetworkAclEntry(
        scope,
        rule_number=200,
        rule_action="ALLOW",
        protocol=6,
        id="private_nacl_all_port_outbound",
        network_acl_id=private_nacl.ref,
        cidr_block=vpc.vpc_cidr_block,
        port_range={"from": 0, "to": 65535},
        egress=True,
    )

    ec2.CfnNetworkAclEntry(
        scope,
        rule_number=210,
        rule_action="ALLOW",
        protocol=-1,
        id="private_nacl_all_port_outside_outbound",
        network_acl_id=private_nacl.ref,
        cidr_block="0.0.0.0/0",
        port_range={"from": 0, "to": 65535},
        egress=True,
    )

    ec2.CfnNetworkAclEntry(
        scope,
        rule_number=220,
        rule_action="ALLOW",
        protocol=6,
        id="private_nacl_https_port_outside_outbound",
        network_acl_id=private_nacl.ref,
        cidr_block="0.0.0.0/0",
        port_range={"from": 443, "to": 443},
        egress=True,
    )


def generate_isolated_nacl_entries(scope, isolated_nacl, private_subnets: List[ec2.ISubnet]):
    inbound_rule_number = 100
    outbound_rule_number = 100
    counter = 1

    for private_subnet in private_subnets:
        # Inbound Isolated NACL Entries
        ec2.CfnNetworkAclEntry(
            scope,
            rule_number=inbound_rule_number,
            rule_action="ALLOW",
            protocol=6,
            id=f"isolated_nacl_rds_port_inbound_{counter}",
            network_acl_id=isolated_nacl.ref,
            cidr_block=private_subnet.ipv4_cidr_block,
            port_range={"from": 3306, "to": 3306},
            egress=False,
        )
        inbound_rule_number += 10

        # Outbound Isolated NACL Entries
        ec2.CfnNetworkAclEntry(
            scope,
            rule_number=outbound_rule_number,
            rule_action="ALLOW",
            protocol=6,
            id=f"isolated_nacl_rds_port_outbound_{counter}",
            network_acl_id=isolated_nacl.ref,
            cidr_block=private_subnet.ipv4_cidr_block,
            port_range={"from": 3306, "to": 3306},
            egress=True,
        )
        outbound_rule_number += 10
        ec2.CfnNetworkAclEntry(
            scope,
            rule_number=outbound_rule_number,
            rule_action="ALLOW",
            protocol=6,
            id=f"isolated_nacl_ephemeral_port_outbound_{counter}",
            network_acl_id=isolated_nacl.ref,
            cidr_block=private_subnet.ipv4_cidr_block,
            port_range={"from": 1024, "to": 65535},
            egress=True,
        )
        outbound_rule_number += 10

        counter += 1
