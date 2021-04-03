from aws_cdk import aws_route53 as route53
import aws_cdk.aws_route53_targets as targets


def generate_lookedup_hosted_zone(scope):
    hosted_zone = route53.HostedZone.from_lookup(scope=scope,
                                                 id="Tier2HostedZone",
                                                 domain_name="apperdevops.com")

    return hosted_zone


def generate_record_in_hosted_zone(scope, hosted_zone: route53.HostedZone, cloudfront_distribution):
    a_record = route53.ARecord(scope, "CloudfrontTier2Route53ARecord",
                               zone=hosted_zone,
                               target=route53.RecordTarget.from_alias(
                                   targets.CloudFrontTarget(cloudfront_distribution)),
                               record_name="jvsantos-tier2.apperdevops.com"
                               )
    return a_record
