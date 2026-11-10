# Cheat sheet: choosing a compute option

Use when a learner asks which compute service fits a workload, or a question hinges on that choice. Verify any detail you cite against the linked page.

## Decision order

1. **Must you control the OS, kernel, licensing or attached hardware** (lift-and-shift, custom agents, specific GPUs)? → **Compute Engine**.
2. **Is it a container that answers HTTP requests or events, with no need for cluster-level control?** → **Cloud Run** (services for requests, jobs for run-to-completion tasks).
3. **Is it a small piece of code triggered by an event** (a file upload, a Pub/Sub message)? → **Cloud Run functions**.
4. **Do you need Kubernetes itself** (Kubernetes APIs, Helm charts, operators, many cooperating services, stateful sets)? → **GKE**; prefer **Autopilot** unless you must manage nodes (then Standard).
5. **Existing App Engine app?** Keep it there; for new apps the exam usually points to Cloud Run.

## Comparison

| Option | You manage | Scales to zero | Typical exam clue |
|---|---|---|---|
| Compute Engine | VMs, OS, patching (or VM Manager), scaling via managed instance groups | No | "legacy", "specific OS", "full control", "GPU", "license tied to cores" |
| GKE Autopilot | Workloads only; Google manages nodes | No (pay per Pod resources) | "Kubernetes", "minimal cluster operations" |
| GKE Standard | Node pools, node configuration | No | "custom node configuration", "DaemonSets on specific nodes" |
| Cloud Run | Container image and settings | Yes | "stateless container", "minimal operational overhead", "pay per use" |
| Cloud Run functions | Function code | Yes | "respond to an event", "single-purpose" |
| App Engine | Code in a supported runtime | Standard environment: yes | "existing App Engine app" |

## Cost and capacity levers

- **Spot VMs**: large discount for fault-tolerant, interruptible work (batch, CI, rendering). They can be preempted at any time, so never use them for a single critical VM.
- **Custom machine types**: pick vCPU and memory independently when predefined shapes waste resources.
- **Managed instance groups (MIGs)**: instance template + autoscaling + autohealing; **regional MIGs** spread VMs across zones for availability.
- **Committed use discounts** for steady usage; **sustained use discounts** apply automatically to eligible VM usage.

## Common traps

- "Minimal operational overhead" rarely means Compute Engine.
- Autoscaling a single VM is not possible; you need a MIG behind a load balancer.
- Spot VMs are not for workloads that cannot tolerate interruption.
- Cloud Run needs a stateless container listening on the port given by `PORT`; local disk is in-memory and not persistent.

## Documentation

- Compute Engine machine families: https://docs.cloud.google.com/compute/docs/machine-resource
- Spot VMs: https://docs.cloud.google.com/compute/docs/instances/spot
- Managed instance groups: https://docs.cloud.google.com/compute/docs/instance-groups
- GKE Autopilot overview: https://docs.cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview
- What is Cloud Run: https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run
- Cloud Run services and functions compared: https://docs.cloud.google.com/run/docs/functions/comparison
- App Engine overview: https://docs.cloud.google.com/appengine/docs/an-overview-of-app-engine
