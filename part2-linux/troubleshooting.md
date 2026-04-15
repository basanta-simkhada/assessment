# Task 2: Linux Troubleshooting Guide (SSH Unresponsive)

## Scenario

- Target Host: '10.0.1.50'
- Symptom: SSH connection timeout
- Assumption: RPM-based Linux (RHEL/CentOS/Amazon Linux)

---

**Step 1: Network Connectivity Test**
_ping -c 5 10.0.1.50_
if ping fails, there is a possibilities for blocked ICMP

_hping -S -p 22 -c 5 10.0.1.50_ OR _nc -zv 10.0.1.50 22_
if either of this commands fail, it might mean ssh service is stopped or port is changed

_nmap -sSV 10.0.1.50_
scan all open ports, services, and their version (only run this command if you doubt the port is changed)

**Step 2: Network Connectivity is OK**
access the server using alternative method, e.g using web consoble, tty console, or relevant:

assumption 1: ssh service is not active

_systemctl status sshd_
_systemctl start sshd_ (if inactive)

assumption 2: ssh service is active but could not login (assuming username and password are correct)

_netstat -talpn_ (check for ssh)
_firewall-cmd --list-services_

OR

_top_
_sar -u 3 10_ (CPU stats)
_sar -r 3 10_ (Memory Stats)
_sar -d 3 10_ (Block device Stats)

_df -Th_ (storage)

_free -h_ (memory)

**Step 3: Log Analysis**
_journalctl -xu sshd_
_tail -n 30 /var/log/secure_
