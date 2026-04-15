# Guide

**Prequisite**
  *pip install boto3*
  *create .aws/credentials file and add keys*

**Simple Step**
  *python ec2_monitor.py*

**Custom Parameter**
  *python ec2_monitor.py --region us-east-1 --threshold 75 --output report.json*

**IAM Permission** (if required)
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "cloudwatch:GetMetricStatistics"
      ],
      "Resource": "\*"
    }
  ]
}
