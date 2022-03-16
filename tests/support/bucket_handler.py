import boto3
import os
import logging
from .files_handler import read_file
from datetime import datetime


OUTPUT_DIR = os.environ["OUTPUT_DIR"]
BUCKET_NAME = os.environ["METRICS_BUCKET_NAME"]
BUILD_NUMBER = os.environ["BUILD_NUMBER"]


def put_logs_on_results_bucket(file_name):
    """
    Put logs an artifacts zip file in S3 bucket
    Return: Path to zip file
    """
    s3_client = boto3.client("s3")
    logs_and_artifacts = read_file(f"{OUTPUT_DIR}/tracer_run.csv", "rb")
    key = f"{BUCKET_NAME}/{datetime.now()}/tracer_run.csv"
    s3_client.put_object(
        Body=logs_and_artifacts,
        Bucket=BUCKET_NAME,
        Key=key,
    )

    return key
