---
layout: ../../layouts/BaseLayout.astro
title: "The Most Dangerous AWS IAM Misconfigurations (And What They Actually Look Like)"
description: "Five AWS IAM misconfigurations that appear in nearly every account — with real policy JSON examples, attacker impact, and least-privilege fixes."
keywords: "AWS IAM misconfiguration, overly permissive IAM policy, AWS least privilege, IAM security audit, wildcard IAM policy"
slug: "blog-02-dangerous-misconfigurations"
author: "Gulo AI"
tags: ["aws", "iam", "security", "cloud", "cybersecurity"]
published: true
type: "article"
publishDate: "2026-06-26T00:00:00Z"
---

<style>
  .post-hero { padding: 3rem 0; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: white; }
  .post-hero .container { max-width: 800px; margin: 0 auto; }
  .post-meta { color: rgba(255,255,255,0.7); margin-bottom: 1rem; font-size: 0.9rem; }
  .post-series { display: inline-block; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); border-radius: 4px; padding: 0.25rem 0.75rem; font-size: 0.8rem; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 1rem; }
  .post-body { max-width: 800px; margin: 0 auto; padding: 3rem 1rem; color: var(--color-gray); line-height: 1.8; }
  .post-body h2 { margin-top: 2.5rem; margin-bottom: 1rem; color: var(--color-dark); }
  .post-body h3 { margin-top: 1.75rem; color: var(--color-dark); }
  .post-body ul, .post-body ol { padding-left: 1.5rem; margin-bottom: 1rem; }
  .post-body li { margin-bottom: 0.4rem; }
  .post-body blockquote { border-left: 4px solid var(--color-primary); padding-left: 1.25rem; margin: 1.5rem 0; font-style: italic; color: #555; }
  .stat-callout { background: #f0f4ff; border-left: 4px solid #4f46e5; padding: 1rem 1.25rem; margin: 1.5rem 0; border-radius: 0 6px 6px 0; }
  .stat-callout strong { display: block; font-size: 1.05rem; margin-bottom: 0.25rem; color: #1e1e3f; }
  .example-block { background: #fafafa; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1.25rem 1.5rem; margin: 1.5rem 0; }
  .example-block h4 { margin: 0 0 0.5rem; color: #c0392b; }
  .cta-block { background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%); color: white; border-radius: 10px; padding: 2rem; margin-top: 3rem; }
  .cta-block h3 { color: white; margin-top: 0; }
  .cta-block p { color: rgba(255,255,255,0.85); }
  .cta-block a { display: inline-block; background: white; color: #0f3460; font-weight: 600; padding: 0.65rem 1.5rem; border-radius: 6px; text-decoration: none; margin-top: 0.5rem; }
  .cta-block a:hover { background: #e8ecf5; }
  .back-link { margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--color-gray-light); }
  .back-link a { color: var(--color-primary); font-weight: 500; }
  .misconfig-label { display: inline-block; background: #fff0f0; border: 1px solid #f5c6c6; border-radius: 4px; padding: 0.2rem 0.6rem; font-size: 0.8rem; letter-spacing: 0.04em; text-transform: uppercase; color: #c0392b; margin-bottom: 0.5rem; }
  .fix-label { display: inline-block; background: #f0fff4; border: 1px solid #b2f0c8; border-radius: 4px; padding: 0.2rem 0.6rem; font-size: 0.8rem; letter-spacing: 0.04em; text-transform: uppercase; color: #1a7340; margin-bottom: 0.5rem; }
</style>

<section class="post-hero">
  <div class="container">
    <div class="post-series">Horizon IAM Risk Series · Part 2 of 5</div>
    <div class="post-meta">June 26, 2026 · 9 min read</div>
    <h1 style="color:white; margin-bottom: 1rem;">The Most Dangerous AWS IAM Misconfigurations (And What They Actually Look Like)</h1>
    <p style="color:rgba(255,255,255,0.8); font-size:1.1rem;">Real policy JSON, real attacker impact, and practical fixes for the five patterns we find in almost every AWS account.</p>
  </div>
</section>

<div class="post-body">

[Part 1 of this series](/blog/blog-01-iam-silent-threat) established why AWS IAM security is the highest-risk surface area in most cloud environments: IAM debt accumulates gradually, it rarely triggers alarms, and it's the most common path attackers exploit. Knowing that the problem exists is step one. Step two is knowing exactly what to look for — because the specific misconfiguration patterns are consistent and identifiable, once you know the signatures.

Here are the five AWS IAM misconfigurations we find most often, along with what they look like in practice and how to fix them.

---

## Misconfiguration #1: Wildcard Actions on Broad Resources

<span class="misconfig-label">High Risk</span>

The wildcard IAM policy is the single most common finding in IAM security audits. It looks like this:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": "*"
    }
  ]
}
```

Or worse, the full account wildcard:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
```

**What an attacker — or an accidental actor — can do with this:** The `s3:*` on `Resource: "*"` variant gives any identity holding this policy unrestricted read, write, delete, and configuration access to every S3 bucket in the account. That includes application data, database backups, CloudTrail logs, and any other bucket that happens to exist. A compromised Lambda function with this policy can enumerate all buckets, exfiltrate their contents, delete objects, or overwrite data — with no restrictions at all. The full wildcard (`Action: "*"`, `Resource: "*"`) is effectively `AdministratorAccess`: the bearer can provision infrastructure, create new IAM roles, modify security groups, or do anything else the AWS APIs allow.

These policies exist because they work. When a developer is trying to ship quickly and can't figure out the exact S3 actions needed, `s3:*` unblocks them immediately. The IAM security debt accumulates one shortcut at a time.

**The fix — apply AWS least privilege:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-app-bucket/uploads/*"
    }
  ]
}
```

Scope actions to only what the identity actually needs, and scope the resource to the specific bucket and prefix. If you're not sure what actions a role actually uses, AWS IAM Access Analyzer and CloudTrail can help you derive the right scope from observed access patterns.

---

## Misconfiguration #2: Overly Permissive Trust Policies

<span class="misconfig-label">High Risk</span>

IAM role trust policies define who can assume a role — but they're easy to misconfigure in ways that open far broader access than intended. A common pattern looks like this:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Or a subtler but equally risky version:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::987654321098:root"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

**The cross-account risk:** The first variant (`Principal: "*"`) allows anyone — any AWS identity from any account, including accounts you have no relationship with — to attempt to assume this role. If the role's permissions policy grants anything useful, this is a critical finding.

The second variant is a more common mistake: trusting the root of an external AWS account. When you trust `arn:aws:iam::987654321098:root`, you're trusting every principal in that account — not just the specific service or user you intended. If any credential in that account is compromised, it can be used to assume your role. Role assumption chains extend this risk: once an attacker assumes the first role, they can potentially assume other roles from it.

**The fix — scope trust to specific principals:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::987654321098:role/specific-deployment-role"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "your-unique-external-id"
        }
      }
    }
  ]
}
```

Always trust a specific role ARN rather than an account root. For third-party integrations, use an `ExternalId` condition to prevent confused deputy attacks. Review cross-account trust relationships regularly — vendor relationships end, CI/CD pipelines change, and trust policies rarely get cleaned up automatically.

---

## Misconfiguration #3: Unused Roles and Users with Active Credentials

<span class="misconfig-label">Medium–High Risk</span>

Not every IAM risk shows up in a policy JSON. Some of the most dangerous findings are identities that simply shouldn't exist anymore.

**The stale identity problem plays out in three common patterns:**

**Departed employees.** An engineer leaves the company. Their IAM user account is disabled or their SSO access is revoked — but their long-lived programmatic access keys remain active. If those keys were stored in a personal laptop, a dotfile, or a local credentials file, they represent an ongoing credential exposure risk that persists long after the employee is gone.

**Decommissioned services.** A microservice is retired. Its IAM execution role stays in place, still attached to policies, still valid for assumption. If someone compromises a system that still holds references to that role, it may be assumable with permissions far broader than expected.

**Old CI/CD integrations.** A migration from Jenkins to GitHub Actions left behind an IAM user with programmatic credentials that were baked into the old pipeline configuration. The new pipeline doesn't use them. The old credentials were never rotated or revoked.

**Manual detection:** AWS provides an IAM credential report (downloadable from the IAM console or via `aws iam generate-credential-report`) that shows last-used timestamps for all IAM users and their access keys. An access key that hasn't been used in 90 days is a candidate for removal; one that hasn't been used in 180+ days is a finding. For roles, IAM Access Advisor shows last-accessed timestamps per role per service.

The challenge is that this is a manual, point-in-time snapshot. Running the credential report tells you the current state — it doesn't alert you when a key goes stale or when a role hasn't been assumed in six months.

---

## Misconfiguration #4: Inline Policies Hiding Permissions

<span class="misconfig-label">Medium Risk</span>

AWS IAM supports two types of policies: managed policies (standalone, reusable, visible in the IAM console's policy list) and inline policies (embedded directly in a user, group, or role). Inline policies create a specific audit challenge.

When you list the managed policies attached to a role, you see all of them immediately. When you look at an IAM user with inline policies, the permissions only appear if you specifically inspect that user's inline policy section. In a large account with dozens or hundreds of users and roles, inline policies are easy to miss during an IAM security audit.

Here's what an inline policy looks like when attached directly to a user — this is the pattern to watch for:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "ec2:StartInstances",
        "ec2:StopInstances",
        "ec2:TerminateInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

There's nothing inherently wrong with these permissions — but if this policy is inline on a user rather than a named managed policy, it won't show up when you run `aws iam list-policies`. You'd need to call `aws iam list-user-policies` for each user, then `aws iam get-user-policy` for each result, to discover it. At scale, this becomes impractical.

**The managed policy alternative:**

```json
{
  "Version": "2012-10-17",
  "Statement": [...]
}
```

Create this as a named managed policy — `EC2InstanceOperatorPolicy`, for example — and attach it to the role or user. Now it's discoverable in the policy list, reusable across identities, and auditable without inspecting individual identities one by one.

As a general practice: prefer managed policies over inline policies. Inline policies should be the exception, not the default, and their presence in an account should itself be a flag for closer review.

---

## Misconfiguration #5: Missing Permission Boundaries on Delegated Roles

<span class="misconfig-label">Medium–High Risk</span>

Permission boundaries are an underused IAM feature that prevent a specific class of privilege escalation. Here's the scenario: you allow a developer or a service to create IAM roles. Without guardrails, they can create a role with any permissions they want — potentially permissions that exceed their own. This is privilege escalation by role creation.

Permission boundaries cap the maximum effective permissions of any role or user, regardless of what policies are attached. A boundary policy defines the ceiling:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*",
        "dynamodb:*",
        "logs:*"
      ],
      "Resource": "*"
    }
  ]
}
```

When this is set as the permission boundary on a delegated role, the role's effective permissions are the intersection of its attached policies and the boundary — even if someone attaches `AdministratorAccess` to the role later, the boundary prevents it from exceeding the defined scope.

In environments where developers or automation can create roles (common in organizations that allow self-service infrastructure), missing permission boundaries mean that the role-creation capability itself becomes a privilege escalation path. A developer with `iam:CreateRole` and `iam:AttachRolePolicy` can grant themselves or their workloads permissions they don't otherwise have. Permission boundaries close that gap.

---

## The Audit Problem

Reading through these five patterns, a reasonable reaction is: "We can check for these manually." And you can — with enough time. But the math doesn't work in your favor.

Even a 20-person engineering organization running a non-trivial AWS workload will have accumulated dozens of IAM roles: execution roles for Lambda functions, instance profiles, deployment roles, cross-account roles for third-party integrations, developer IAM users, service accounts. Stack on managed policies, inline policies, resource-based policies on S3 buckets and SQS queues, and trust relationships across development, staging, and production accounts — and you're looking at 100+ distinct IAM configurations to review.

A manual IAM security audit produces a point-in-time snapshot. You review your current state, document findings, and remediate what you can. Three months later, the environment has changed: new services deployed, new trust relationships created, old roles not yet cleaned up. The snapshot is already out of date. Without continuous visibility, you're always working from stale data.

This is the gap between "we did an IAM review last quarter" and actually managing IAM risk as a continuous posture rather than a periodic exercise.

---

## Detecting These Patterns Automatically

The five misconfigurations in this post — wildcard actions, overly permissive trust policies, stale identities, hidden inline policies, and missing permission boundaries — are detectable. They have signatures. An automated IAM security audit can identify all of them systematically, across every role and policy in your account, in minutes.

That's exactly what Horizon IAM Risk Analyzer is built to do. It connects to your AWS environment, maps your IAM posture, and surfaces these specific overly permissive IAM policy patterns with AI-powered remediation guidance — including the corrected policy JSON you need to fix each finding.

<div class="cta-block">
  <h3>Stop Guessing What's in Your IAM</h3>
  <p>Horizon IAM Risk Analyzer detects wildcard policies, overly broad trust relationships, stale credentials, hidden inline policies, and missing permission boundaries — automatically, with remediation guidance built in.</p>
  <a href="#">[Start your free 14-day trial on AWS Marketplace →]</a>
</div>

**Up next — Part 3: Privilege Escalation Attack Paths in AWS IAM.** Once an attacker has a foothold in your environment, specific IAM configurations allow them to escalate from limited access to full account control without ever touching a vulnerability. We'll walk through the actual techniques and show you what the policies that enable them look like.

<div class="back-link">
  <a href="/blog">← Back to Blog</a>
</div>

</div>
