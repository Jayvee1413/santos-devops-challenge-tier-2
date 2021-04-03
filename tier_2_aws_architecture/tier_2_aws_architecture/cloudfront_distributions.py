from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk.aws_cloudfront import SourceConfiguration, CustomOriginConfig, ViewerCertificate, OriginProtocolPolicy, \
    Behavior, CloudFrontAllowedMethods, CfnDistribution


def generate_cloudfront_distribution(scope, certificate, ecs_url):
    cloudfront_distribution = cloudfront.CloudFrontWebDistribution(scope=scope,
                                                                   id="JVSANTOSTier2CloudfrontDistribution",
                                                                   default_root_object="",
                                                                   origin_configs=[SourceConfiguration(
                                                                       custom_origin_source=CustomOriginConfig(
                                                                           domain_name=ecs_url,
                                                                           origin_protocol_policy=OriginProtocolPolicy.MATCH_VIEWER,
                                                                           http_port=80,
                                                                           https_port=443
                                                                       ),
                                                                       behaviors=[Behavior(
                                                                           allowed_methods=CloudFrontAllowedMethods.ALL,
                                                                           is_default_behavior=True,
                                                                           forwarded_values=CfnDistribution.ForwardedValuesProperty(
                                                                               query_string=True,
                                                                               cookies=CfnDistribution.CookiesProperty(
                                                                                   forward="all"),
                                                                               headers=["*"]
                                                                           )
                                                                       )]
                                                                   )],
                                                                   viewer_certificate=ViewerCertificate.from_acm_certificate(
                                                                       certificate=certificate,
                                                                       aliases=["jvsantos-tier2.apperdevops.com"]),
                                                                   )
    return cloudfront_distribution
