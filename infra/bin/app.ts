#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { AgentCoreRiskStack } from "../lib/agentcore-risk-stack";

const app = new cdk.App();

new AgentCoreRiskStack(app, "AgentCoreRiskAssessment", {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION ?? "us-east-1",
  },
  description:
    "Multi-agent financial risk assessment demo — AgentCore Runtime, Memory, MCP tools",
});
