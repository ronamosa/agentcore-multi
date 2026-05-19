import * as cdk from "aws-cdk-lib";
import * as iam from "aws-cdk-lib/aws-iam";
import * as ecr from "aws-cdk-lib/aws-ecr";
import * as ssm from "aws-cdk-lib/aws-ssm";
import { Construct } from "constructs";

/**
 * CDK stack for the AgentCore Financial Risk Assessment demo.
 *
 * Creates:
 * - IAM roles for each agent runtime (least-privilege Bedrock + Memory access)
 * - ECR repositories for agent container images
 * - SSM parameters for runtime configuration
 *
 * AgentCore Runtime and Memory resources are created via the AgentCore SDK
 * in the setup script (scripts/setup-agentcore.py) since they are API-only
 * resources with no CloudFormation support yet.
 */
export class AgentCoreRiskStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const agents = [
      "supervisor",
      "credit-analyst",
      "income-verifier",
      "market-analyst",
      "compliance-officer",
    ];

    // Bedrock model access policy (shared)
    const bedrockPolicy = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
      ],
      resources: ["*"],
    });

    // AgentCore Memory policy
    const memoryPolicy = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        "bedrock:CreateMemory",
        "bedrock:GetMemory",
        "bedrock:ListMemories",
        "bedrock:DeleteMemory",
        "bedrock:SaveMemories",
        "bedrock:RetrieveMemories",
      ],
      resources: ["*"],
    });

    // AgentCore Runtime policy
    const runtimePolicy = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        "bedrock:CreateAgentRuntime",
        "bedrock:GetAgentRuntime",
        "bedrock:ListAgentRuntimes",
        "bedrock:DeleteAgentRuntime",
        "bedrock:InvokeAgentRuntime",
        "bedrock:UpdateAgentRuntime",
      ],
      resources: ["*"],
    });

    // ECR pull policy (for runtime to pull agent images)
    const ecrPolicy = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
      ],
      resources: ["*"],
    });

    for (const agent of agents) {
      // IAM role per agent
      const role = new iam.Role(this, `${agent}-role`, {
        roleName: `agentcore-risk-${agent}`,
        assumedBy: new iam.CompositePrincipal(
          new iam.ServicePrincipal("bedrock.amazonaws.com"),
          new iam.ServicePrincipal("ecs-tasks.amazonaws.com")
        ),
        description: `AgentCore runtime role for ${agent}`,
      });

      role.addToPolicy(bedrockPolicy);
      role.addToPolicy(ecrPolicy);

      if (agent === "supervisor") {
        role.addToPolicy(memoryPolicy);
        role.addToPolicy(runtimePolicy);
      }

      // ECR repo per agent
      const repo = new ecr.Repository(this, `${agent}-repo`, {
        repositoryName: `agentcore-risk/${agent}`,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
        emptyOnDelete: true,
        lifecycleRules: [
          { maxImageCount: 5, description: "Keep last 5 images" },
        ],
      });

      // SSM params for runtime discovery
      new ssm.StringParameter(this, `${agent}-role-arn`, {
        parameterName: `/agentcore-risk/${agent}/role-arn`,
        stringValue: role.roleArn,
      });
      new ssm.StringParameter(this, `${agent}-ecr-uri`, {
        parameterName: `/agentcore-risk/${agent}/ecr-uri`,
        stringValue: repo.repositoryUri,
      });
    }

    // Outputs
    new cdk.CfnOutput(this, "Region", {
      value: this.region,
      description: "Deployment region",
    });
  }
}
