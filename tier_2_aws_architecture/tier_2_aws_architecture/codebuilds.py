from aws_cdk import aws_codebuild as codebuild
from aws_cdk.aws_codebuild import BuildSpec, BuildEnvironmentVariable, BuildEnvironmentVariableType, LinuxBuildImage


def generate_buildspec():
    buildspec = {
        "version": 0.2,
        "phases": {
            "install": {
                "runtime-versions": {
                    "nodejs": "latest"
                },
                "commands": [
                    "echo Entered the installing phase..."
                ],
                "finally": [
                    "echo This always runs even if the update or install command fails"
                ]
            },
            "pre_build": {
                "commands": [
                    "nohup /usr/local/bin/dockerd &",
                    "sleep 30",
                    "export REGION=${AWS_REGION}",
                    "export ACCOUNT_ID=$(echo $CODEBUILD_BUILD_ARN | cut -f5 -d ':')",
                    "aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"
                ],
            },
            "build": {
                "commands": [
                    "echo Build Started `date`",
                    "cd express-minapp/",
                    "echo HOST=$HOST >> .env",
                    "echo USERNAME=$USERNAME >> .env",
                    "echo PASSWORD=$PASSWORD >> .env",
                    "echo DATABASE=$DATABASE >> .env",
                    "echo PORT=80 >> .env",
                    "docker build -t $REPO_NAME:$IMAGE_TAG .",
                    "docker tag $REPO_NAME:$IMAGE_TAG $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:$IMAGE_TAG"
                ],
            },
            "post_build": {
                "commands": [
                    "echo Build Completed `date`",
                    "docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:$IMAGE_TAG",
                    "echo Create Image Definitions File",
                    'echo [{\\"name\\": \\"$CONTAINER_NAME\\", \\"imageUri\\": \\"$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:$IMAGE_TAG\\"}] > imagedefinitions.json'
                ]
            }
        },
        "artifacts": {
            "files": [
                "package.json",
                "src/index.js",
                "src/middlewares.js",
                "node_modules/**/*",
                "package-lock.json",
                ".env",
                "imagedefinitions.json",
            ],
            "name": "express-minapp",
            "base-directory": "express-minapp"
        },
        "cache": {
            "paths": [
                "node_modules/**/*"
            ]
        }
    }

    return BuildSpec.from_object(buildspec)


def generate_codebuild_project(scope, role, db_secret, ecr_repo_name, ecr_repo_tag="latest", container_name="web"):
    codebuild_project = codebuild.PipelineProject(scope=scope,
                                                  id="JVSANTOSTier2CodebuildProject",
                                                  build_spec=generate_buildspec(),
                                                  project_name="JVSANTOSTier2",
                                                  role=role,
                                                  environment=codebuild.BuildEnvironment(
                                                      build_image=LinuxBuildImage.AMAZON_LINUX_2_3,
                                                      privileged=True),
                                                  environment_variables=
                                                  {
                                                      "HOST": BuildEnvironmentVariable(
                                                          value=f"{db_secret.secret_name}:host",
                                                          type=BuildEnvironmentVariableType.SECRETS_MANAGER),
                                                      "USERNAME": BuildEnvironmentVariable(
                                                          value=f"{db_secret.secret_name}:username",
                                                          type=BuildEnvironmentVariableType.SECRETS_MANAGER),
                                                      "PASSWORD": BuildEnvironmentVariable(
                                                          value=f"{db_secret.secret_name}:password",
                                                          type=BuildEnvironmentVariableType.SECRETS_MANAGER),
                                                      "DATABASE": BuildEnvironmentVariable(
                                                          value=f"{db_secret.secret_name}:dbname",
                                                          type=BuildEnvironmentVariableType.SECRETS_MANAGER),
                                                      "PORT": BuildEnvironmentVariable(
                                                          value=1337,
                                                          type=BuildEnvironmentVariableType.PLAINTEXT),
                                                      "REPO_NAME": BuildEnvironmentVariable(
                                                          value=ecr_repo_name,
                                                          type=BuildEnvironmentVariableType.PLAINTEXT),
                                                      "IMAGE_TAG": BuildEnvironmentVariable(
                                                          value=ecr_repo_tag,
                                                          type=BuildEnvironmentVariableType.PLAINTEXT),
                                                      "CONTAINER_NAME": BuildEnvironmentVariable(
                                                          value=container_name,
                                                          type=BuildEnvironmentVariableType.PLAINTEXT),
                                                  }
                                                  )

    return codebuild_project
