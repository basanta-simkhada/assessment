# Task 1: Infrastructure as Code Analysis (Terraform Code)

**1. Architectural Problems**
**Critical**
a. No Internet Gateway & NAT Architecture
  *Why it’s a problem*
    - Instances in “public” subnets does not have outbound internet access.
    - Architecture is incomplete and non-functional for real-world workloads.

b. No Separation of Public and Private Tiers
  *Why it’s a problem*
    - Violates standard 3-tier architecture
    - Database exposure risk increases

c. No Load Balancer
  *Why it's a problem*
    - No traffic distribution
    - No high availability entry point

d. No Auto Scaling
  *Why it's a problem*
    - Cannot handle load spikes
    - Wastes cost during low traffic

e. Missing DB Subnet Group
  *Why it's a problem*
    - AWS assigns default subnets (often public)
    - Lack of control over DB placement

**Warnings**
a. No logical resource ordering
b. No Tagging Strategy
c. No Infrastructure Modularity

**2. Security Gaps**
**Critical**
a. Open SSH Access to the World
  *Why it's a problem*
    - Exposes instances to brute-force attacks
    - Common entry point for compromise

b. Overly Permissive Egress Rules
  *Why it's a problem*
    - Allows unrestricted outbound traffic
    - Enables data exfiltration

c. Database Using Same Security Group as Web Tier
  *Why it's a problem*
    - DB exposed to same ingress rules as web servers
    - Potential lateral movement risk

d. Hardcoded Database Credentials
  *Why it's a problem*
    - Credential leakage risk
    - Violates secrets management practices

e. No Encryption for RDS
  *Why it's a problem*
    - Data at rest is unprotected
    - Compliance violations

f. No Backup Strategy
  *Why it's a problem*
    - No point-in-time recovery
    - Data loss risk

g. Deletion Protection Disabled
  *Why it's a problem*
    - Accidental DB deletion possible

h. Skip Final Snapshot Enabled
  *Why it's a problem*
    - Data loss during destroy operations

i. No S3 Security Configuration
  *Why it's a problem*
    - Data exposure risk
    - No recovery for accidental deletion

**Warning**
a. No IAM Roles for EC2
b. No Monitoring & Logging
c. HTTP open without HTTPS

**Recommendations**
a. Standardize with Modular Terraform Architecture
b. Isolate Environments with Separate State
c. Enforce Security and Configuration Baselines
d. Parameterize and Manage Environment-Specific Configuration
e. Implement CI/CD Pipeline for Infrastructure (if possible)
