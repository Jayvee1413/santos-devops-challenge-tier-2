from aws_cdk import aws_codestarconnections as codestarconnection


def generate_codestar_connection(scope):
    codestar_connection = codestarconnection.CfnConnection(scope=scope,
                                                           id="CodeStarConnection",
                                                           connection_name="jvsantostier2",
                                                           provider_type="GitHub"
                                                           )
    return codestar_connection
