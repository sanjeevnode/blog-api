"""
Run on container startup — creates the S3/RustFS bucket if it doesn't exist.
Retries for up to 60s so it survives a slow RustFS cold-start.
"""
import os
import time
import boto3
from botocore.exceptions import ClientError

ENDPOINT = os.getenv("S3_ENDPOINT_URL", "http://rustfs:9000")
ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "rustfsadmin")
SECRET_KEY = os.getenv("S3_SECRET_KEY", "rustfsadmin")
BUCKET = os.getenv("S3_BUCKET_NAME", "blog-media")


def ensure_bucket() -> None:
    s3 = boto3.client(
        "s3",
        endpoint_url=ENDPOINT,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name="ap-south-1",
    )
    for attempt in range(12):
        try:
            try:
                s3.head_bucket(Bucket=BUCKET)
                print(f"[bucket] '{BUCKET}' already exists")
            except ClientError as e:
                # 404 means the bucket doesn't exist yet
                if e.response["Error"]["Code"] == "404":
                    s3.create_bucket(Bucket=BUCKET)
                    # Make bucket publicly readable so image URLs work in browser
                    s3.put_bucket_policy(
                        Bucket=BUCKET,
                        Policy=f'''{{
                            "Version":"2012-10-17",
                            "Statement":[{{
                                "Effect":"Allow",
                                "Principal":"*",
                                "Action":"s3:GetObject",
                                "Resource":"arn:aws:s3:::{BUCKET}/*"
                            }}]
                        }}''',
                    )
                    print(f"[bucket] created '{BUCKET}'")
                else:
                    raise
            return
        except Exception as exc:
            print(f"[bucket] attempt {attempt + 1}/12 failed: {exc}")
            time.sleep(5)
    raise RuntimeError(f"Could not reach RustFS after 60s")


if __name__ == "__main__":
    ensure_bucket()
