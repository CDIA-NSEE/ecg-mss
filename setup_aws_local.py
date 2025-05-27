import os
import time
from datetime import datetime

import boto3
from typing import List
from dotenv import load_dotenv
from pytz import UTC

from populate_entities import User, UserRole, EcgExam, Gender, ReportType, EcgReport

load_dotenv()

bucket_name = os.getenv("BUCKET_NAME")
dynamodb_table_name = os.getenv("DYNAMO_TABLE")

time.sleep(2)

print("Conectando ao DynamoDB Local...")
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    endpoint_url='http://dynamodb-local:8000'
)

print("Criando tabela exemplo...")
try:
    # Create the table
    table = dynamodb.create_table(
        TableName=dynamodb_table_name,
        KeySchema=[
            {
                'AttributeName': 'PK',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'SK',
                'KeyType': 'RANGE'
            }
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'type-index',
                'KeySchema': [
                    {
                        'AttributeName': 'type',
                        'KeyType': 'HASH'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'PK',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'SK',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'type',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.wait_until_exists()
    print(f"Tabela '{dynamodb_table_name}' criada com sucesso.")
    print("Index available:", [index['IndexName'] for index in table.global_secondary_indexes])
except Exception as e:
    table = dynamodb.Table(dynamodb_table_name)
    print(f"Tabela já existe ou erro: {e}")

print("Conectando ao MinIO...")
s3 = boto3.client(
    's3',
    region_name='us-east-1',
    endpoint_url='http://minio:9000'
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
    User(name="Felipe Carillo", email="felipecarillo@nsee.imt", password="1234", role=UserRole.DOCTOR),
    User(name="Íris Melero", email="irismelero@nsee.imt", password="1234", role=UserRole.DOCTOR),
    User(name="Douglas", email="douglas@nsee.imt", password="1234", role=UserRole.DOCTOR),
    User(name="Dr. Paulo", email="paulo@nsee.imt", password="1234", role=UserRole.DOCTOR),
]

print("Criando exames de teste...")
test_exams: List[EcgExam] = [
    EcgExam(
        id="exam1",
        file_path="exams/exam1.ecg",
        made_at=datetime.now(UTC),
        gender=Gender.MALE,
        birth_date="1990-01-01",
        amplitude="1.0",
        speed="25",
        reports=[EcgReport(
            report=ReportType.ALTERACOES_INESPECIFICAS_ST_T,
            created_at=datetime.now(UTC),
        )]
    )
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

for exam in test_exams:
    try:
        exam_dynamo = exam.to_dynamo()
        print(exam_dynamo)
        table.put_item(Item=exam_dynamo)
        print(f"Exame '{exam.id}' criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar exame '{exam.id}': {e}")

print("Desconectando do DynamoDB Local...")
dynamodb.meta.client.close()
print("Desconectando do MinIO...")
s3.close()
