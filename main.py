from typing import Union 
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader 
from services.bill import Bill 

import boto3

from config.config import config

app = FastAPI()

header_schema = APIKeyHeader(name="x-key")

client = boto3.client(
    'ce',
    aws_access_key_id=config["aws_access_key_id"],
    aws_secret_access_key=config["aws_secret_access_key"],
    region_name='us-east-1',
)

@app.get("/bills")
async def read_root(
    key: str = Depends(header_schema),
    start_date: str = "",
    end_date: str = "",
):
    if key != config["auth_key"]:
        raise HTTPException(status_code=403) 

    bill = Bill(client)

    rsp = bill.get_billing_info(start_date, end_date)

    return rsp["ResultsByTime"]
