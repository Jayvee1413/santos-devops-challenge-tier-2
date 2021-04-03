# santos-devops-challenge-tier-2

The Cloudformation Templates are in `cfn_templates`

1. VPC Stack: `aws cloudformation deploy --template cfn_templates/JVSANTOSTier2VPCAwsArchitectureStack.json --stack-name JVSANTOSTier2VPCAwsArchitectureStack --capabilities CAPABILITY_IAM --profile apper --region ap-southeast-1`
2. Update CodeStar Connection via the AWS Console
3. ECS Stack: `aws cloudformation deploy --template cfn_templates\JVSANTOSTier2ECSAwsArchitectureStack.json --stack-name JVSANTOSTier2ECSAwsArchitectureStack --capabilities CAPABILITY_NAMED_IAM --profile apper --region ap-southeast-1`
4. CICD Stack: `aws cloudformation deploy --template cfn_templates\JVSANTOSTier2CICDAwsArchitectureStack.json --stack-name JVSANTOSTier2CICDAwsArchitectureStack --capabilities CAPABILITY_NAMED_IAM --profile apper --region ap-southeast-1`
5. Since we cannot use the generated ACM Certificate above for our Cloudfront Distribution, we would have to create a certificate in `us-east-1` region: US-East-1 ACM Certificate Stack: `aws cloudformation deploy --template cfn_templates\JVSANTOSTier2ACMCertificateUS-EAST-1Stack.json --stack-name JVSANTOSTier2ACMCertificateUS-EAST-1Stack  --profile apper --region us-east-1`
6. Take note of the generated ARN from `5`. (Currently: `arn:aws:acm:us-east-1:329511059546:certificate/b933533b-4c3f-4d15-a114-100f7458fc47`)
7. Edit `JVSANTOSTier2CDNAwsArchitectureStack.json` line `63` for the value of the ACM Certificate generated in `5`.
8. CDN Stack: `aws cloudformation deploy --template cfn_templates\JVSANTOSTier2CDNAwsArchitectureStack.json --stack-name JVSANTOSTier2CDNAwsArchitectureStack --capabilities CAPABILITY_NAMED_IAM --profile apper --region ap-southeast-1`