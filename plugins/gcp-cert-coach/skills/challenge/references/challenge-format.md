# Challenge format

## Task template

```
Challenge: <short title>
Concepts: <concept titles>

Goal
<one or two sentences: the outcome, in business terms>

Constraints
- <limits that force the right design: least privilege, no external IPs, region, budget, no keys>

Success criteria
1. <observable result that a verification command can show>
2. ...
(3–5 criteria)

Verification (run these and paste the output)
<read-only commands: describe, list, get-iam-policy, curl to an endpoint>

Submit
- A short narrative: what you created and why, in the order you did it.
- The output of each verification command, with project ids, emails and other identifiers replaced by [REDACTED].
- Screenshots are optional.

Cost and cleanup
<what may cost money; the delete commands or console steps to run afterwards>
```

## Writing good criteria

- Each criterion is checkable from the verification output (for example "the service account has no user-managed keys" is checked by a keys list command).
- At least one criterion tests the constraint that a careless solution would break (least privilege, no public access, private networking).
- Do not hint at the commands that build the solution. Verification commands may name resources but must not create or change anything.

## Example (shortened)

```
Challenge: Least-privilege reader VM
Concepts: Service accounts; Roles

Goal
A VM must read objects from one Cloud Storage bucket and nothing else, without any service account key.

Constraints
- Dedicated service account, no basic roles, no keys.
- Access granted on the bucket, not on the project.

Success criteria
1. The VM runs as the dedicated service account.
2. That account holds only an object-read role, on the bucket.
3. The account has no user-managed keys.
4. Reading an object from the VM works; writing fails.

Verification
gcloud compute instances describe <vm> --zone <zone> --format="value(serviceAccounts[].email)"
gcloud storage buckets get-iam-policy gs://<bucket>
gcloud iam service-accounts keys list --iam-account <sa-email> --managed-by=user
```

## Scoring table (review message)

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | VM runs as dedicated account | met (1) | describe output shows the dedicated account |
| 2 | Only object read on bucket | partly (0.5) | role correct, but also granted on the project |

Score = mean of results. Bonus when score ≥ 0.5: 15 + 10 × score points per linked concept (for example score 0.75 → 22.5 points), capped at level 100.
