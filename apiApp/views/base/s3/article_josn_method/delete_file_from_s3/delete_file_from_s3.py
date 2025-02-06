
import os
import django
from django.conf import settings
from botocore.exceptions import NoCredentialsError
import boto3
import json

def delete_file_from_s3(file_path):

    s3_options = settings.STORAGES['custom_s3']['OPTIONS']

    # s3_client = boto3.client(
    #     's3',
    #     aws_access_key_id='AKIA6GBMBSQAVBQZMKF2',
    #     aws_secret_access_key='MnWSXROk051tdTH4HRBt/SLCWHB3+pPXr9l9H9MV',
    #     region_name='us-east-1'  # e.g., 'us-east-1'
    # )
    s3_client = boto3.client(
        's3',
        aws_access_key_id=s3_options['access_key'],
        aws_secret_access_key=s3_options['secret_key'],
        region_name=s3_options['region_name']
    )
    if file_path.startswith("s3://"):
        key = file_path[len("s3://") + len(settings.AWS_STORAGE_BUCKET_NAME) + 1:]  # Remove "s3://<bucket-name>/"

        try:
            # Delete the object from the bucket
            s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
            print(f"File {file_path} deleted successfully.")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
    else:
        print("Invalid file path. Must start with 's3://'.")