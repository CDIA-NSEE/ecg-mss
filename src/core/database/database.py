import boto3
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer


class Database:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table("nsee-ecg")

    @staticmethod
    def serialize(item: dict) -> dict:
        """Serialize the item for DynamoDB"""
        serializer = TypeSerializer()
        return {k: serializer.serialize(v) for k, v in item.items()}

    @staticmethod
    def deserialize(item: dict) -> dict:
        """Deserialize the item from DynamoDB"""
        deserializer = TypeDeserializer()
        return {k: deserializer.deserialize(v) for k, v in item.items()}
