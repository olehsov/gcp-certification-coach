# Cheat sheet: IAM role types and service accounts

Use when a learner asks about roles, permissions or service accounts, or a question hinges on least privilege. Verify any detail you cite against the linked page.

## Model

- An **allow policy** binds **principals** to **roles** on a resource. Roles are collections of **permissions**.
- Policies are set on the organization, folders, projects or individual resources and are **inherited downward**. Effective access is the union of the allow policies on the resource and its ancestors; a lower level cannot remove access granted higher up.
- **Deny policies** can block specific permissions regardless of allow policies.
- Principals: Google accounts, service accounts, Google groups, Google Workspace or Cloud Identity domains, `allUsers` / `allAuthenticatedUsers`, and workforce or workload identity pool identities. Grant roles to **groups**, not individuals.

## Role types

| Type | What it is | Use |
|---|---|---|
| Basic | Owner, Editor, Viewer: broad, project-wide | Avoid in production; too coarse for least privilege |
| Predefined | Service-specific roles maintained by Google (for example `roles/compute.viewer`, `roles/storage.objectViewer`) | Default choice |
| Custom | Your own list of permissions, created at organization or project level (not folder) | When no predefined role is narrow enough; you maintain it as permissions change |

## Service accounts

- An identity for workloads, not people. Types: **user-managed**, **default** (created when some services are enabled), and **service agents** (Google-managed, used by services on your behalf).
- **Attach** a service account to the resource (VM, Cloud Run service, GKE workload) and let code get short-lived credentials from the environment. Avoid downloading **service account keys**; organizations can block key creation with an organization policy.
- Workloads outside Google Cloud should use **Workload Identity Federation** instead of keys.
- **Impersonation**: a principal with the Service Account Token Creator role on a service account can obtain short-lived tokens for it. Attaching a service account to a resource requires the **Service Account User** role on it.
- Service accounts are also **resources**: control who can use or manage them with IAM on the service account itself.
- Give each workload its own service account with only the roles it needs; avoid using the default Compute Engine service account with broad roles.

## Common traps

- "View only" → a `*.viewer` predefined role, not Editor.
- "Temporary access for an engineer" → impersonation or a time-bound IAM condition, not a shared key.
- Removing a role at the project level does not remove the same role granted at a folder or organization level.
- Use **Policy Troubleshooter** to explain why a principal has (or lacks) access, and **role recommendations** to remove unused permissions.

## Documentation

- IAM overview: https://docs.cloud.google.com/iam/docs/overview
- Roles and permissions: https://docs.cloud.google.com/iam/docs/roles-overview
- Principals: https://docs.cloud.google.com/iam/docs/principals-overview
- Deny policies: https://docs.cloud.google.com/iam/docs/deny-overview
- Resource hierarchy: https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy
- Service accounts overview: https://docs.cloud.google.com/iam/docs/service-account-overview
- Service account types: https://docs.cloud.google.com/iam/docs/service-account-types
- Best practices for service accounts: https://docs.cloud.google.com/iam/docs/best-practices-service-accounts
- Attach service accounts to resources: https://docs.cloud.google.com/iam/docs/attach-service-accounts
- Service account impersonation: https://docs.cloud.google.com/iam/docs/service-account-impersonation
- Workload Identity Federation: https://docs.cloud.google.com/iam/docs/workload-identity-federation
- Restricting service account usage: https://docs.cloud.google.com/organization-policy/restrict-service-accounts
- Policy Troubleshooter: https://docs.cloud.google.com/policy-intelligence/docs/troubleshoot-access
- Role recommendations: https://docs.cloud.google.com/policy-intelligence/docs/role-recommendations-overview
