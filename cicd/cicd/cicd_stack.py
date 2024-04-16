from select import POLLERR
from constructs import Construct
from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_ssm as ssm,
    aws_iam as iam,
    aws_codecommit as codecommit,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
)

import os

# # s3 bucket artifact
S3_BUCKET_ARTIFACT="mule-pipeline-artifact-"

class CicdStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # s3 bucket
        aws_account=os.environ["CDK_DEFAULT_ACCOUNT"]
        bucket_artifact_name=S3_BUCKET_ARTIFACT+aws_account

        bucket = s3.Bucket(self, bucket_artifact_name, 
                           bucket_name=bucket_artifact_name,
                           block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                           encryption=s3.BucketEncryption.S3_MANAGED,
                           versioned=True,
                           removal_policy=RemovalPolicy.RETAIN
                          )
        
        # repository
        repo = codecommit.Repository(
            self, 'mule-1',
            repository_name = "mule-1",
            code = codecommit.Code.from_directory("../mule-1", "main"),
        )

        # pipeline
        pipeline = codepipeline.Pipeline(self, "mule-1-pipeline", artifact_bucket = bucket)

        source_output = codepipeline.Artifact("SourceArtifact")
        source_stage = pipeline.add_stage(stage_name="Source")
        source_stage.add_action(codepipeline_actions.CodeCommitSourceAction(
            action_name="Source",
            output=source_output,
            repository=repo,
            trigger=codepipeline_actions.CodeCommitTrigger.POLL,
        ))

        # Codebuild project role
        build_project_role = iam.Role(self, "Role", 
            role_name = "codebuild-mule-1-role",
            assumed_by = iam.ServicePrincipal("codebuild.amazonaws.com")
        )

        build_project_policy = iam.ManagedPolicy(self, "Policy",
            managed_policy_name = "codebuild-mule-1-policy",
            statements = [iam.PolicyStatement(
                actions = ["logs:*", "s3:*", "codebuild:*", "ssm:*"],
                resources=["*"]
            )]
        )
        build_project_role.add_managed_policy(build_project_policy)

        # Codebuild project
        build_project = codebuild.PipelineProject(self, "mule-1-build",
            environment=codebuild.BuildEnvironment(privileged=True),
            role = build_project_role
        )

        
        build_output = codepipeline.Artifact("BuildArtifact")
        build_stage = pipeline.add_stage(stage_name="Build")
        build_stage.add_action(codepipeline_actions.CodeBuildAction(
            action_name="Build",
            input = source_output,
            project = build_project,
            outputs = [build_output],
        ))

        # parameter store
        parameter_store = ssm.StringParameter(self, "mule-1-settings",
            parameter_name = "mule-1-settings",
            string_value='<?xml version="1.0" encoding="UTF-8"?><settings/>',
        )



