#!/usr/bin/env python3

import boto3
import argparse
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from botocore.exceptions import BotoCoreError, ClientError
from datetime import datetime, timedelta, timezone

def setup_logging(level: str) -> None:
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def load_config(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        if isinstance(data, list):
            if not data:
                raise ValueError("Config file contains empty list")
            return data[0]

        if not isinstance(data, dict):
            raise ValueError("Config must be a JSON object")

        return data

    except Exception as e:
        logging.error(f"Failed to load config file: {e}")
        raise

def get_running_instances(ec2_client) -> List[Dict[str, Any]]:
    instances = []
    try:
        paginator = ec2_client.get_paginator('describe_instances')

        for page in paginator.paginate(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        ):
            for reservation in page['Reservations']:
                for instance in reservation['Instances']:
                    instances.append(instance)

    except (BotoCoreError, ClientError) as e:
        logging.error(f"Error fetching EC2 instances: {e}")
        raise

    return instances

def extract_instance_info(instance: Dict[str, Any]) -> Dict[str, str]:
    instance_id = instance.get("InstanceId", "")
    instance_type = instance.get("InstanceType", "")

    name = "N/A"
    for tag in instance.get("Tags", []):
        if tag["Key"] == "Name":
            name = tag["Value"]
            break

    return {
        "InstanceId": instance_id,
        "InstanceType": instance_type,
        "Name": name
    }

def get_cpu_metrics(
    cloudwatch_client,
    instance_id: str
) -> Optional[Dict[str, float]]:
    try:
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=1)

        response = cloudwatch_client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Average', 'Minimum', 'Maximum']
        )

        datapoints = response.get("Datapoints", [])

        if not datapoints:
            return None

        avg = sum(d["Average"] for d in datapoints) / len(datapoints)
        min_val = min(d["Minimum"] for d in datapoints)
        max_val = max(d["Maximum"] for d in datapoints)

        return {
            "Average": round(avg, 2),
            "Minimum": round(min_val, 2),
            "Maximum": round(max_val, 2)
        }

    except (BotoCoreError, ClientError) as e:
        logging.error(f"Error fetching metrics for {instance_id}: {e}")
        return None

def generate_report(
    instances: List[Dict[str, Any]],
    cloudwatch_client,
    threshold: int
) -> List[Dict[str, Any]]:

    report = []

    for instance in instances:
        info = extract_instance_info(instance)
        metrics = get_cpu_metrics(cloudwatch_client, info["InstanceId"])

        if metrics is None:
            logging.warning(f"No metrics for instance {info['InstanceId']}")
            continue

        flagged = metrics["Average"] > threshold

        report.append({
            "InstanceId": info["InstanceId"],
            "Name": info["Name"],
            "InstanceType": info["InstanceType"],
            "CPUUtilization": metrics,
            "HighCPU": flagged
        })

    return report

def save_report(report: List[Dict[str, Any]], output_file: str) -> None:
    try:
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=4)
        logging.info(f"Report saved to {output_file}")
    except Exception as e:
        logging.error(f"Failed to save report: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="EC2 Monitoring Script")

    parser.add_argument("--region", help="AWS region", required=False)
    parser.add_argument("--threshold", type=int, help="CPU threshold", required=False)
    parser.add_argument("--output", default="report.json", help="Output file")
    parser.add_argument("--config", default="config.json", help="Config file path")
    parser.add_argument("--log-level", default="INFO", help="Logging level")

    args = parser.parse_args()

    setup_logging(args.log_level)

    config = load_config(args.config)

    region = args.region or config.get("regions", ["us-east-1"])[0]
    threshold = args.threshold or config.get("alert_threshold", 80)

    logging.info(f"Using region: {region}")
    logging.info(f"CPU threshold: {threshold}")

    try:
        ec2_client = boto3.client("ec2", region_name=region)
        cloudwatch_client = boto3.client("cloudwatch", region_name=region)

        instances = get_running_instances(ec2_client)

        if not instances:
            logging.warning("No running instances found.")
            return

        report = generate_report(instances, cloudwatch_client, threshold)

        save_report(report, args.output)

    except Exception as e:
        logging.critical(f"Fatal error: {e}")
        exit(1)


if __name__ == "__main__":
    main()