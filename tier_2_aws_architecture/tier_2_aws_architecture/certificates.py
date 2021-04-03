from aws_cdk import aws_certificatemanager as certificatemanager


def generate_acm_certificate(scope, hosted_zone):
    certificate = certificatemanager.Certificate(scope=scope,
                                                 id="Tier2ACMCertificate",
                                                 domain_name="jvsantos-tier2.apperdevops.com",
                                                 subject_alternative_names=["*.jvsantos-tier2.apperdevops.com"],
                                                 validation=certificatemanager.CertificateValidation.from_dns(
                                                     hosted_zone),
                                                 )
    return certificate
