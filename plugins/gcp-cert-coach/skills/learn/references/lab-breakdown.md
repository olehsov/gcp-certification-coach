# Lab breakdown format

For each step the learner gives (a command, a console action or a short instruction), write a numbered block:

1. **Step** — the command or action, quoted briefly (only what is needed to identify it).
2. **What it does** — the resource it creates or changes and the important flags or fields.
3. **Why** — the reason this step is in the lab: what would fail or be missing without it.
4. **Other ways** — at least one alternative (console vs `gcloud` vs Terraform, a different flag, a managed option) and when to prefer it.
5. **In production** — what a team would do differently: least-privilege service accounts, no external IPs, labels, infrastructure as code, monitoring, cleanup.

After the steps:

- **What the lab teaches**: two or three sentences linking the steps to the exam-guide objectives.
- **Check yourself**: two short questions the learner can answer from the breakdown (no answers given unless asked).
- **Cleanup**: commands or console actions to delete what the lab created, so the learner's own project does not keep billing.
- **Documentation**: the official pages for each resource type used.

Rules:

- Explain from documentation, not from the lab text. Do not reproduce lab instructions; quote only the fragment that identifies a step.
- If the pasted output contains project ids, account emails or keys, do not repeat them; refer to them generically ("your project id") and remind the learner to redact such values when sharing.
- If a step looks wrong or outdated (a deprecated command or flag), say so and give the current form with a link.
