from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as codepipeline_actions


def generate_pipeline_stages(codebuild_project, codestar_connection, ecs_service):
    source_output = codepipeline.Artifact("SourceOutput")
    source_stage = codepipeline.StageProps(stage_name="Source",
                                           actions=[
                                               codepipeline_actions.BitBucketSourceAction(
                                                   connection_arn=codestar_connection.attr_connection_arn,
                                                   output=source_output,
                                                   repo="tier2",
                                                   owner="Jayvee1413",
                                                   branch="main",
                                                   action_name="Github",
                                                   code_build_clone_output=True,
                                                   run_order=1),
                                           ],
                                           )
    codebuild_output = codepipeline.Artifact("CodebuildOutput")
    codebuild_stage = codepipeline.StageProps(stage_name="Build",
                                              actions=[
                                                  codepipeline_actions.CodeBuildAction(
                                                      input=source_output,
                                                      project=codebuild_project,
                                                      outputs=[codebuild_output],
                                                      action_name="codebuild",
                                                      run_order=2,
                                                  )
                                              ])
    deploy_stage = codepipeline.StageProps(stage_name="Deploy",
                                           actions=[
                                               codepipeline_actions.EcsDeployAction(
                                                   service=ecs_service,
                                                   input=codebuild_output,
                                                   action_name="ecs-deploy",
                                                   run_order=3,
                                               )
                                           ])
    return [source_stage, codebuild_stage, deploy_stage]


def generate_pipeline(scope, bucket, role, codebuild_project, codestar_connection, ecs_service):
    pipeline = codepipeline.Pipeline(scope=scope,
                                     id="JVSANTOSCodePipelineTier2",
                                     artifact_bucket=bucket,
                                     pipeline_name="jvsantos-pipeline-tier2",
                                     role=role,
                                     stages=generate_pipeline_stages(codebuild_project=codebuild_project,
                                                                     codestar_connection=codestar_connection,
                                                                     ecs_service=ecs_service)
                                     )
    # pipeline.
    return pipeline
