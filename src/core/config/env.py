import os
from typing import Literal

from dotenv import load_dotenv

load_dotenv()


class Environment:
    STAGE: Literal['test', 'dev', 'uat', 'prod'] = os.environ.get("STAGE", "dev")

    # AWS
    BUCKET_NAME: str = os.environ.get("BUCKET_NAME")
    DYNAMO_TABLE: str = os.environ.get("DYNAMO_TABLE")

    # JWT
    JWT_SECRET: str = os.environ.get("JWT_SECRET")
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM")


ENV = Environment()
