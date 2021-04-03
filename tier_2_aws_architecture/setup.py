import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="tier_2_aws_architecture",
    version="0.0.1",

    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "tier_2_aws_architecture"},
    packages=setuptools.find_packages(where="tier_2_aws_architecture"),

    install_requires=[
        "aws-cdk.core==1.94.1",
        "aws-cdk.aws_ec2==1.94.1",
        "aws-cdk.aws_codestarconnections==1.94.1",
        "aws-cdk.aws_rds==1.94.1",
        "aws-cdk.aws_certificatemanager==1.94.1",
        "aws-cdk.aws_route53_targets==1.94.1",
        "aws-cdk.aws_route53==1.94.1",
        "aws-cdk.aws_ecr==1.94.1",
        "aws-cdk.aws_ecs==1.94.1",
        "aws-cdk.aws_ecs_patterns==1.94.1",
        "aws-cdk.aws_codepipeline==1.94.1",
        "aws-cdk.aws_codepipeline_actions==1.94.1",
        "aws-cdk.aws_codebuild==1.94.1",
        "aws-cdk.aws_codedeploy==1.94.1",
        "aws-cdk.aws_elasticloadbalancingv2==1.94.1",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
