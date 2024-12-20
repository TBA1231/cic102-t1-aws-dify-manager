
import boto3
from datetime import datetime, timedelta

# Initialize CloudWatch client
cloudwatch = boto3.client('cloudwatch')

# Define the time range for metrics
end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=1)  # Last 1 hour

# Fetch CPUUtilization metrics
response = cloudwatch.get_metric_statistics(
    Namespace='AWS/EC2',
    MetricName='CPUUtilization',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': 'i-0abcd1234efgh5678'  # Replace with your instance ID
        }
    ],
    StartTime=start_time,
    EndTime=end_time,
    Period=300,  # Data granularity in seconds (5 minutes)
    Statistics=['Average'],  # Available: 'Average', 'Sum', 'Maximum', 'Minimum', 'SampleCount'
    Unit='Percent'
)

# Parse and display the data
for point in response['Datapoints']:
    print(f"Time: {point['Timestamp']}, Average CPU Utilization: {point['Average']}%")

from fastapi import FastAPI

app = FastAPI()

@app.get("/ec2/metrics/{instance_id}")
async def get_ec2_metrics(instance_id: str):
    # Initialize CloudWatch client
    cloudwatch = boto3.client('cloudwatch')

    # Define the time range for metrics
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=1)

    # Fetch CPUUtilization metrics
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {'Name': 'InstanceId', 'Value': instance_id}
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average'],
        Unit='Percent'
    )

    # Format and return the data
    data_points = [
        {"Timestamp": point["Timestamp"], "Average": point["Average"]}
        for point in response.get("Datapoints", [])
    ]
    return {"InstanceId": instance_id, "Metrics": data_points}
