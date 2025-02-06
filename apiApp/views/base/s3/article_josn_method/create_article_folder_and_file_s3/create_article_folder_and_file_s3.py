
import os
import django
from django.conf import settings
from botocore.exceptions import NoCredentialsError
import boto3
import json


def create_article_folder_and_file_s3(data):

    # Extract the id and other fields from the input data
    domain_slug_id = data.get("domain_slug_id")
    article_slug_id = data.get("article_slug_id")
    wp_content = data.get("wp_content")
    wp_excerpt = data.get("wp_excerpt")

    # Validate input data
    if not all([domain_slug_id, article_slug_id, wp_content, wp_excerpt]):
        raise ValueError("Missing required fields in the input data")

    s3_options = settings.STORAGES['custom_s3']['OPTIONS']

    # Ensure the S3 bucket name is configured
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    if not bucket_name:
        print("AWS_STORAGE_BUCKET_NAME is not set in Django settings.")

    # Define the folder structure in S3
    s3_folder_path = f"{domain_slug_id}/{article_slug_id}"
    json_file_name = "article_content.json"
    s3_file_path = f"{s3_folder_path}/{json_file_name}"

    # Prepare the content for the JSON file
    article_data = {
        "wp_content": wp_content,
        "wp_excerpt": wp_excerpt
    }

    # Serialize the data to JSON
    json_data = json.dumps(article_data, indent=4)

    # s3_client = boto3.client(
    #     's3',
    #     aws_access_key_id='AKIA6GBMBSQAVBQZMKF2',
    #     aws_secret_access_key='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',
    #     region_name='us-east-1'
    # )

    s3_client = boto3.client(
        's3',
        aws_access_key_id=s3_options['access_key'],
        aws_secret_access_key=s3_options['secret_key'],
        region_name=s3_options['region_name']
    )

    
    try:
        s3_client.put_object(Bucket=bucket_name, Key=s3_file_path, Body=json_data, ContentType='application/json')
        print(f"JSON file uploaded to S3 at: s3://{bucket_name}/{s3_file_path}")
    except NoCredentialsError:
        raise Exception("AWS credentials not found.")
    except Exception as e:
        raise Exception(f"An error occurred while uploading to S3: {e}")

    a = f"s3://{bucket_name}/{s3_file_path}"
    print(a,'50365')
    # Return the S3 file path
    return f"s3://{bucket_name}/{s3_file_path}"












