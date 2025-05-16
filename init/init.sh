#!/bin/sh

echo "Instalando dependências..."
pip install pytz
pip install boto3
pip install pydantic
pip install python-dotenv

echo "Executando script de criação de recursos..."
python create_resources.py

echo "Finalizado!"
