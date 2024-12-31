import boto3
import fastapi
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException

app = fastapi()

accountId = ''

# List all EC2 instances

def get_paginator_describe_instances():
    client = boto3.client('ec2')
    paginator = client.get_paginator('describe_instances')
    response_iterator = paginator.paginate(
        DryRun=True,
        Filters=[
            {
                'tag-key ': 'cic102-t1',
            },
        ],
        PaginationConfig={
            'PageSize': 100,
        }
    )

# Get CPU metrics for an instance in the past 7 days

def get_ec2_cpu_metrics(instance_id):
    client = boto3.client('cloudwatch')
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': instance_id,
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'cic102-t1/EC2',
                        'MetricName': 'cpu',
                        'Dimensions': [
                            {
                                'Name': 'instance Id',
                                'Value': instance_id
                            },
                        ]
                    },
                    'Period': 3600,
                    'Stat': 'avarage',
                    'Unit': 'Percent'
                }
            }
        ],
        StartTime=datetime.today() - datetime.timedelta(days = 7),
        EndTime=datetime.today()
        LabelOptions={
            'Timezone': '+0800'
        }
    )

@app.get("/instances")
def list_instances():
    try:
        instances = get_paginator_describe_instances()
        return {"instances": instances}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing instances: {str(e)}")

@app.get("/metrics/{instance_id}")
def fetch_metrics(instance_id: str):
    try:
        metrics = get_ec2_cpu_metrics(instance_id)
        return {"metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching metrics: {str(e)}")
