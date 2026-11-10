# Explanation format

Use these headings in this order, translated into the learner's language. Keep the whole answer to what fits on one or two screens; cut detail before cutting a section.

1. **What it is**: one or two sentences, plain words.
2. **How it works**: the mechanism (components, data flow, scope: global, regional or zonal; who manages what). A small table or ASCII sketch when it helps.
3. **When to use it**: two to four typical situations, phrased like exam scenarios ("you need X with minimal operations").
4. **Alternatives**: the services or options it is confused with, and the deciding difference for each.
5. **Best practices**: production habits (least privilege, high availability, cost, automation).
6. **Exam angle**: which exam-guide objective it maps to (from the tracker's module `sections` when known) and the clue words that point to it in questions.
7. **Common traps**: two or three mistakes or near-miss answers.
8. **Try it** (optional): one or two `gcloud` or console steps the learner can run in their own project, with a cleanup note. Never run commands on the learner's behalf.
9. **Documentation**: the official pages you fetched, as links.

## Example (shortened)

> **What it is** — Cloud NAT lets resources without external IP addresses reach the internet for outbound traffic.
>
> **How it works** — It is a regional, software-defined service configured on a Cloud Router … no NAT VM in the data path …
>
> **Alternatives** — Private Google Access (reach Google APIs only, no NAT needed); external IPs on each VM (inbound exposure) …
>
> **Documentation** — https://docs.cloud.google.com/nat/docs/overview

Fill every section from fetched documentation; this example only shows the shape.
