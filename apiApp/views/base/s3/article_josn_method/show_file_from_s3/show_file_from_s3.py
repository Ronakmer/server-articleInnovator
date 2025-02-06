

import os
import django
from django.conf import settings
from botocore.exceptions import NoCredentialsError
import boto3
import json


def show_file_from_s3(s3_url):
    try:
        s3_options = settings.STORAGES['custom_s3']['OPTIONS']


        bucket_name, *key_parts = s3_url[5:].split("/", 1)

        # Combine the remaining parts to reconstruct the key
        key = key_parts[0] if key_parts else ""

        # s3_client = boto3.client(
        #         's3',
        #         aws_access_key_id='AKIA6GBMBSQAVBQZMKF2',
        #         aws_secret_access_key='MnWSXROk051tdTH4HRBt/SLCWHB3+pPXr9l9H9MV',
        #         region_name='us-east-1'  # e.g., 'us-east-1'
        #     )
        
        
        s3_client = boto3.client(
            's3',
            aws_access_key_id=s3_options['access_key'],
            aws_secret_access_key=s3_options['secret_key'],
            region_name=s3_options['region_name']
        )
         
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        # Read the object's content
        data = response['Body'].read().decode('utf-8')
        # Parse JSON content
        json_data = json.loads(data)
        print("JSON Content:", json_data)
        return json_data
    except Exception as e:
        print("Error fetching data:", str(e))
