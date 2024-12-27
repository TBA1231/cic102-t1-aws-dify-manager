import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "aws_access_key_id": os.environ['AWS_ACCESS_KEY_ID'],
    "aws_secret_access_key": os.environ['AWS_SECRET_ACCESS_KEY'],
    "auth_key": os.environ['AUTH_KEY']
}