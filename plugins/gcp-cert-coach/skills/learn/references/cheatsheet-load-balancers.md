# Cheat sheet: choosing a load balancer

Use when a learner asks which Cloud Load Balancing product fits, or a question hinges on that choice. Verify any detail you cite against the linked page.

## Decision order

1. **HTTP or HTTPS traffic (layer 7)** → **Application Load Balancer**.
   - Clients on the internet, backends in several regions, one anycast IP → **global external** Application Load Balancer.
   - Internet clients, backends in one region, regional compliance → **regional external**.
   - Clients inside your VPC → **internal** Application Load Balancer (regional or cross-region).
2. **TCP with TLS offload or a proxy in front (layer 4)** → **proxy Network Load Balancer** (external or internal).
3. **TCP, UDP or other IP protocols where the backend must see the client's source IP, or traffic must pass through unchanged** → **passthrough Network Load Balancer** (regional; external or internal).

## Quick facts

| Product | Layer | Scope | Proxy or passthrough |
|---|---|---|---|
| External Application LB | 7 | Global or regional | Proxy |
| Internal Application LB | 7 | Regional or cross-region | Proxy |
| External proxy Network LB | 4 | Global or regional | Proxy |
| Internal proxy Network LB | 4 | Regional or cross-region | Proxy |
| External passthrough Network LB | 4 | Regional | Passthrough |
| Internal passthrough Network LB | 4 | Regional | Passthrough |

- **Cloud CDN** and **Cloud Armor** (WAF, DDoS protection) attach to external Application Load Balancers.
- Global external load balancing uses the **Premium** Network Service Tier; Standard tier is regional.
- Health checks need firewall rules that allow Google's health-check probe ranges.
- Backends are usually **managed instance groups** (autoscaling, autohealing), network endpoint groups, or serverless NEGs (Cloud Run).

## Common traps

- URL-path or host-based routing needs an Application Load Balancer (URL map), not a Network Load Balancer.
- A passthrough load balancer does not terminate TLS; a proxy does.
- Internal traffic between tiers in one VPC usually wants an internal load balancer, not an external one with firewall restrictions.

## Documentation

- Load balancing overview: https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview
- Choose a load balancer: https://docs.cloud.google.com/load-balancing/docs/choosing-load-balancer
- Application Load Balancer: https://docs.cloud.google.com/load-balancing/docs/application-load-balancer
- Proxy Network Load Balancer: https://docs.cloud.google.com/load-balancing/docs/proxy-network-load-balancer
- Passthrough Network Load Balancer: https://docs.cloud.google.com/load-balancing/docs/passthrough-network-load-balancer
- Cloud CDN: https://docs.cloud.google.com/cdn/docs/overview
- Cloud Armor: https://docs.cloud.google.com/armor/docs/cloud-armor-overview
- Network Service Tiers: https://docs.cloud.google.com/network-tiers/docs/overview
