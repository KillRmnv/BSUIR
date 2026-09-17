import os
import logging
from typing import Optional

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

_client = None


def _get_client():
    global _client
    if _client is None:
        endpoint = os.environ.get("MINIO_ENDPOINT", "localhost:9000")
        access_key = os.environ.get("MINIO_ACCESS_KEY", "minioadmin")
        secret_key = os.environ.get("MINIO_SECRET_KEY", "minioadmin")
        _client = boto3.client(
            "s3",
            endpoint_url=f"http://{endpoint}",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name="us-east-1",
        )
    return _client


def _get_external_endpoint() -> str:
    """Return the externally accessible MinIO endpoint (for presigned URLs)."""
    return os.environ.get("MINIO_EXTERNAL_ENDPOINT", "localhost:9000")


def _get_bucket() -> str:
    return os.environ.get("MINIO_BUCKET", "documents")


def ensure_bucket():
    """Create the bucket if it doesn't exist."""
    client = _get_client()
    bucket = _get_bucket()
    try:
        client.head_bucket(Bucket=bucket)
    except ClientError:
        try:
            client.create_bucket(Bucket=bucket)
            logger.info("Created MinIO bucket: %s", bucket)
        except ClientError as e:
            logger.error("Failed to create bucket %s: %s", bucket, e)
            raise


def upload_file(file_bytes: bytes, object_name: str, content_type: str = "application/octet-stream") -> str:
    """Upload file to MinIO. Returns the object key."""
    client = _get_client()
    bucket = _get_bucket()
    client.put_object(
        Bucket=bucket,
        Key=object_name,
        Body=file_bytes,
        ContentType=content_type,
    )
    logger.info("Uploaded %s to s3://%s/%s", object_name, bucket, object_name)
    return object_name


def get_presigned_url(object_name: str, expires: int = 3600) -> Optional[str]:
    """Generate a presigned URL for downloading a file."""
    client = _get_client()
    bucket = _get_bucket()
    try:
        url = client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": object_name},
            ExpiresIn=expires,
        )
        external = _get_external_endpoint()
        internal = os.environ.get("MINIO_ENDPOINT", "localhost:9000")
        if external != internal:
            url = url.replace(f"http://{internal}", f"http://{external}")
        return url
    except ClientError as e:
        logger.error("Failed to generate presigned URL for %s: %s", object_name, e)
        return None


def download_file(object_name: str) -> Optional[bytes]:
    """Download file from MinIO. Returns file bytes or None."""
    client = _get_client()
    bucket = _get_bucket()
    try:
        response = client.get_object(Bucket=bucket, Key=object_name)
        return response["Body"].read()
    except ClientError as e:
        logger.error("Failed to download %s: %s", object_name, e)
        return None


def delete_file(object_name: str) -> bool:
    """Delete file from MinIO."""
    client = _get_client()
    bucket = _get_bucket()
    try:
        client.delete_object(Bucket=bucket, Key=object_name)
        return True
    except ClientError as e:
        logger.error("Failed to delete %s: %s", object_name, e)
        return False


def object_exists(object_name: str) -> bool:
    """Check if an object exists in MinIO."""
    client = _get_client()
    bucket = _get_bucket()
    try:
        client.head_object(Bucket=bucket, Key=object_name)
        return True
    except ClientError:
        return False


def upload_text(text: str, object_name: str) -> str:
    """Upload text content to MinIO as UTF-8. Returns the object key."""
    return upload_file(text.encode("utf-8"), object_name, content_type="text/plain; charset=utf-8")


def download_text(object_name: str) -> Optional[str]:
    """Download text content from MinIO. Returns string or None."""
    data = download_file(object_name)
    if data is None:
        return None
    return data.decode("utf-8")
