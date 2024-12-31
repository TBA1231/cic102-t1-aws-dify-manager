from typing import Union 
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader 
from services.bill import Bill 
from services.cloudwatch import Cloudwatch

import boto3

from config.config import config

app = FastAPI(
    servers=[
        {"url": "http://localhost:8000/"},
        {"url": "https://hpuy2z372d.ap-south-1.awsapprunner.com/"},
    ],
)

header_schema = APIKeyHeader(name="x-key")

ce_client = boto3.client(
    'ce',
    aws_access_key_id=config["aws_access_key_id"],
    aws_secret_access_key=config["aws_secret_access_key"],
    region_name='ap-south-1',
)

ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=config["aws_access_key_id"],
    aws_secret_access_key=config["aws_secret_access_key"],
    region_name='ap-south-1',
)

cloudwatch_client = boto3.client(
    'cloudwatch',
    aws_access_key_id=config["aws_access_key_id"],
    aws_secret_access_key=config["aws_secret_access_key"],
    region_name='ap-south-1',
)

@app.get("/bills")
async def read_root(
    key: str = Depends(header_schema),
    start_date: str = "",
    end_date: str = "",
):
    if key != config["auth_key"]:
        raise HTTPException(status_code=403) 

    bill = Bill(ce_client)

    rsp = bill.get_billing_info(start_date, end_date)

    return rsp["ResultsByTime"]

@app.get("/cpu_usage")
async def read_root(
    key: str = Depends(header_schema),
    start_date: str = "",
    end_date: str = "",
):
    if key != config["auth_key"]:
        raise HTTPException(status_code=403) 

    cloudwatch = Cloudwatch(ec2_client, cloudwatch_client)
    instances = cloudwatch.get_ec2_info()['Reservations'][0]['Instances']
    rsp = []
    for instance in instances:
        rsp.append({'instance Id': instance["InstanceId"], 'CPU Usage': cloudwatch.get_ec2_cpu_usage(instance["InstanceId"], start_date, end_date)['Messages'][0]['Value']})
    return rsp
