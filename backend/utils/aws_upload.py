# backend/utils/aws_upload.py

import boto3
import os
from dotenv import load_dotenv

# Load AWS credentials from .env
load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
REGION = "ap-south-1"  # Change this if you're using a different region

# Initialize boto3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION
)

def upload_to_s3(file, filename):
    try:
        s3.upload_fileobj(file, AWS_BUCKET_NAME, filename)
        file_url = f"https://{AWS_BUCKET_NAME}.s3.{REGION}.amazonaws.com/{filename}"
        return file_url
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None
