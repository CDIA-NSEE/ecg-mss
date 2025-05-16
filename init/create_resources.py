import os
import time
import boto3
from typing import List
from populate_user import User
from dotenv import load_dotenv

load_dotenv()

bucket_name = os.getenv("BUCKET_NAME")
dynamodb_table_name = os.getenv("DYNAMO_TABLE")

time.sleep(2)

print("Conectando ao DynamoDB Local...")
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://dynamodb-local:8000',
    region_name='us-east-1',
    aws_access_key_id='fake',
    aws_secret_access_key='fake'
)

print("Criando tabela exemplo...")
try:
    table = dynamodb.create_table(
        TableName=dynamodb_table_name,
        KeySchema=[{'AttributeName': 'PK', 'KeyType': 'HASH'}, {'AttributeName': 'SK', 'KeyType': 'RANGE'}],
        AttributeDefinitions=[
            {'AttributeName': 'PK', 'AttributeType': 'S'},
            {'AttributeName': 'SK', 'AttributeType': 'N'}
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    table.wait_until_exists()
    print(f"Tabela '{dynamodb_table_name}' criada com sucesso.")
except Exception as e:
    table = dynamodb.Table(dynamodb_table_name)
    print(f"Tabela já existe ou erro: {e}")

print("Conectando ao MinIO...")
s3 = boto3.client(
    's3',
    endpoint_url='http://minio:9000',
    aws_access_key_id='nsee',
    aws_secret_access_key='nsee',
    region_name='us-east-1'
)

print("Criando bucket exemplo...")
try:
    s3.create_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' criado com sucesso.")
except Exception as e:
    print(f"Bucket já existe ou erro: {e}")

# Criando usuários de teste
print("Criando usuários de teste...")
test_users: List[User] = [
    User(name="Felipe Carillo", email="felipecarillo@nsee.imt", password="1234"),
]


# Clear table
def clear_table(table):
    print(f"Clearing table '{table.name}'...")
    try:
        response = table.scan()
        items = response.get('Items', [])
        with table.batch_writer() as batch:
            for item in items:
                batch.delete_item(Key={'PK': item['PK'], 'SK': item['SK']})
        print(f"Table '{table.name}' cleared successfully.")
    except Exception as e:
        print(f"Error clearing table: {e}")


clear_table(table)

for user in test_users:
    try:
        user_dynamo = user.to_dynamo()
        print(user_dynamo)
        table.put_item(Item=user_dynamo)
        print(f"Usuário '{user.email}' criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar usuário '{user.email}': {e}")
