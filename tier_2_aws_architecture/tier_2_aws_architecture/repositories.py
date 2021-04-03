from aws_cdk import aws_ecr as ecr


def generate_ecr_repository(scope):

    repo = ecr.Repository(scope=scope, id="JVSANTOSTier2ECRRepo",
                          repository_name="jvbsantos-tier2")

    return repo