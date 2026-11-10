# Numeric facts

The single source for numbers that skills of this plugin state or test: capacities, availability targets, minimum durations, limits. Every value was checked against the linked official page. Use a number only when it is in this table or on a page fetched in this session. A number from neither source must not be the tested point of a question, and an explanation marks it as unverified. When a fetched page disagrees with this table, trust the page, say so, and record feedback (`kind: "bug"`).

| Topic | Fact | Source |
|---|---|---|
| Dedicated Interconnect | Circuits of 10 Gbps, 100 Gbps or 400 Gbps; up to 8 circuits of one type per connection (80, 800 or 3200 Gbps); the circuit type cannot be changed after creation | https://docs.cloud.google.com/network-connectivity/docs/interconnect/concepts/dedicated-overview |
| Partner Interconnect | VLAN attachments from 50 Mbps to 50 Gbps; the sizes offered depend on the partner and location | https://docs.cloud.google.com/network-connectivity/docs/interconnect/concepts/overview |
| HA VPN | 99.99% availability SLA for most topologies (some topologies get 99.9%) | https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview |
| Classic VPN | 99.9% availability SLA | https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview |
| Cloud VPN tunnel | Up to 250,000 packets per second per tunnel (ingress plus egress), roughly 1 to 3 Gbps depending on packet size | https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview |
| Cloud Storage classes | Minimum storage duration: Standard none, Nearline 30 days, Coldline 90 days, Archive 365 days | https://docs.cloud.google.com/storage/docs/storage-classes |
| Cloud Storage objects | Maximum object size 5 TiB | https://docs.cloud.google.com/storage/quotas |
| Cloud Storage soft delete | Default retention 7 days; configurable from 7 to 90 days, or 0 to disable | https://docs.cloud.google.com/storage/docs/soft-delete |
| Cloud Logging buckets | `_Required`: 400 days, not configurable. `_Default` (project): 30 days by default, configurable from 1 to 3650 days | https://docs.cloud.google.com/logging/quotas |
| BigQuery time travel | 7 days by default, configurable from 2 to 7 days; fail-safe adds 7 more days, not configurable | https://docs.cloud.google.com/bigquery/docs/time-travel |
| Spot VMs | No minimum or maximum runtime unless you set one; preemption notice 0 seconds (default) or 120 seconds; shutdown best effort up to 30 seconds | https://docs.cloud.google.com/compute/docs/instances/spot |
| Preemptible VMs | Always stopped after 24 hours of runtime; Spot VMs are the recommended successor | https://docs.cloud.google.com/compute/docs/instances/preemptible |
| Cloud Run request timeout | Default 5 minutes (300 seconds); maximum 60 minutes (3600 seconds) | https://docs.cloud.google.com/run/docs/configuring/request-timeout |
| Service account keys | At most 10 keys per service account; the limit cannot be changed | https://docs.cloud.google.com/iam/quotas |

Service-level percentages for Cloud SQL, Spanner and Compute Engine are not listed: fetch the product's SLA page before stating one.
