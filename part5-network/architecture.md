# Task 5: DNS Architecture

                        ┌──────────────────────────────┐
                        │        Internet Users        │
                        │     (Nepal / South Asia)     │
                        └──────────────┬───────────────┘
                                       │ DNS Query
                                       ▼
                        ┌──────────────────────────────┐
                        │        Amazon Route 53       │
                        │  - Public Hosted Zone        │
                        │  - Latency-based Routing     │
                        │  - Health Checks             │
                        │  - Failover Policy           │
                        └──────────────┬───────────────┘
                                       │
               ┌───────────────────────┴────────────────────────┐
               │                                                │
               ▼                                                ▼
   ┌──────────────────────────┐                    ┌──────────────────────────┐
   │ Primary Region (ap-south-1) │                │ Secondary Region (ap-southeast-1) │
   │ Mumbai (LOW latency)     │                    │ Singapore (fallback)     │
   └─────────────┬────────────┘                    └─────────────┬────────────┘
                 │                                               │
     ┌──────────────────────────┐                    ┌──────────────────────────┐
     │ EC2 / ALB + Unbound DNS  │                    │ EC2 / ALB + Unbound DNS  │
     │ (Primary Resolver Tier)  │                    │ (Secondary Resolver Tier)│
     └─────────────┬────────────┘                    └─────────────┬────────────┘
                   │                                               │
                   └─────────────── Health Checks ────────────────┘

**Important Components**
  *Amazon Route 53 (Core Layer)*
    a. Public Hosted Zone (authoritative DNS)
    b. Routing policies:
        Latency-based routing
        Failover routing (Primary/Secondary)
    c. Built-in global DNS infrastructure (high availability)

  *Regional DNS Layer*
    a. Deploy Unbound (or managed alternative) in 2 regions:

  *Health Checks*
    a. Route 53 HTTP/TCP health checks against:
        /health endpoint on DNS resolver
        or port 53 (TCP/UDP via custom check)
    b. Integrated with routing policies
