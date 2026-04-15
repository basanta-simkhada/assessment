# My Details

**Name:**       Basanta Simkhada
**Contact:**    +977 9849613656

## Part 1

This task requires reviewing an existing Terraform configuration to identify architectural weaknesses and security misconfigurations. It involves assessing issues such as poor environment separation, insecure IAM usage, and missing production-grade safeguards. Findings must be categorized by severity and accompanied by remediation recommendations. The final objective is to ensure the infrastructure is production-ready, secure, and scalable.

## Part 2

Task 2 focuses on diagnosing and resolving an SSH timeout issue on host 10.0.1.50. The troubleshooting process begins with validating basic network reachability using ICMP ping and TCP port checks (SSH port 22), followed by service and port verification using tools like netcat or hping, and optionally service discovery via nmap if port mismatch is suspected. If connectivity is confirmed but SSH remains inaccessible, the next step is to access the system through an alternative console to verify whether the sshd service is running, check firewall rules, and assess system health metrics such as CPU, memory, and disk usage. Finally, log inspection using journalctl and /var/log/secure helps identify authentication failures, service crashes, or configuration-related errors contributing to the SSH failure.

## Part 3

This task involves creating a monitoring solution for AWS EC2 instances, typically using AWS SDK (boto3). The script should evaluate instance health metrics such as CPU utilization and trigger alerts based on defined thresholds. It must securely handle AWS credentials and support configurable parameters like region and threshold values. The goal is to provide basic automated infrastructure monitoring and alerting capability.

## Part 4

This task requires building a Bash script to analyze Nginx access logs from /var/log/nginx/access.log. The script should compute metrics such as top 10 client IPs, most requested endpoints, and the proportion of 4xx/5xx errors. It must also support variations in log formats and produce a clean summary report. The output is intended for quick operational insights into traffic and errors.

## Part 5

This task involves designing a highly available DNS system for an organization that currently relies on a single Unbound DNS server. The objective is to eliminate single points of failure by introducing redundancy using AWS Route 53. It should include primary and secondary failover routing policies with health checks to automatically redirect traffic during outages. Additionally, latency optimization is required, considering users in Nepal, along with a cost-aware design.

## Part 6

This task focuses on improving an existing GitHub Actions workflow that currently performs basic testing and deployment. The goal is to enhance reliability, security, and deployment control in the pipeline. Improvements may include proper job separation, caching dependencies, secure handling of secrets, and controlled deployment strategies instead of direct server pushes. It aims to make deployments more robust and production-ready.
