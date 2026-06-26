"""
upload_referentiel.py
Dépose le référentiel statique d'Anfa (lignes, arrêts, bus, tarifs)
dans un bucket MinIO local.
"""
from pathlib import Path
import boto3
from botocore.exceptions import ClientError
MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ACCESS_KEY = "anfa-app-key"
MINIO_SECRET_KEY = "anfa-app-secret-2026"
BUCKET_NAME = "anfa-raw"
s3 = boto3.client(
"s3",
endpoint_url=MINIO_ENDPOINT,
aws_access_key_id=MINIO_ACCESS_KEY,
aws_secret_access_key=MINIO_SECRET_KEY,
region_name="us-east-1",
)