# muleapp-1

This document is to describe how to do a codepipeline to deploy a mulesoft app to CludeHub 2.0.

## Repo structure

- cicd: cdk to create infrastructure including S3, CodeCommit, CodeBuild, CodePipeline etc
- muleapp-1: the demo code of mulesoft application 

## Prerequisites

- AWS Account
- AWS IAM user with uploaded SSH public keys for AWS CodeCommit


## Steps:

```
cd cicd
pip3 install -r requirements.txt
cdk synth
cdk deploy
```

After a while, the codepipeline will be deployed on your acccount and it will automatially run in first time. At the first time, the execution will be failed due to some configurations;

Do changes on muleapp-1:

- setting.xml:
    copy setting.xml content to parameter store "mule-1-settings" and update the {username}, {passworld} to your mulesoft username and passowrd

- pom.xml:
    change the {BusinessGroupID} to your Business Group ID in mulesoft "Access Management/Business Groups/Seeting/Business Group ID"  and commit to codecommit repo;


Run codepipeline to deploy your appliction




