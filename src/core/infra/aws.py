import boto3

from core.config.env import ENV


class AWS:
    @staticmethod
    def get_dynamodb_resource():
        if ENV.STAGE == "test":
            return boto3.resource(
                "dynamodb",
                endpoint_url="http://dynamodb-local:8000",
                region_name="us-east-1",
                aws_access_key_id="fake",
                aws_secret_access_key="fake",
            )
        return boto3.resource("dynamodb")

    @staticmethod
    def get_s3_client():
        if ENV.STAGE == "test":
            return boto3.client(
                "s3",
                endpoint_url="http://minio:9000",
                aws_access_key_id="minioadmin",
                aws_secret_access_key="minioadmin",
                region_name="us-east-1",
            )
        return boto3.client("s3")
