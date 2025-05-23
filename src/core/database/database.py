from boto3.dynamodb.types import TypeSerializer, TypeDeserializer

from core.infra.aws import AWS
from core.config.env import ENV


class Database:
    def __init__(self):
        self.dynamodb = AWS.get_dynamodb_resource()
        self.table = self.dynamodb.Table(ENV.DYNAMO_TABLE)

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
