import jwt
from pytz import UTC
from typing import Union
from datetime import datetime, timedelta

from core.config.env import ENV


class JWToken:
    jwt_secret = ENV.JWT_SECRET
    jwt_algorithm = ENV.JWT_ALGORITHM

    @classmethod
    def encode(
            cls,
            user_id: Union[str, dict],
            exp_days: int = 1,
            exp_hours: int = 0,
            exp_minutes: int = 0,
    ) -> str:
        payload = {
            'user_id': user_id,
            'exp': datetime.now(tz=UTC) + timedelta(days=exp_days, hours=exp_hours, minutes=exp_minutes)
        }
        return jwt.encode(payload, cls.jwt_secret, algorithm=cls.jwt_algorithm)

    @classmethod
    def decode(cls, access_token: str) -> Union[Union[str, dict], bool]:
        try:
            return jwt.decode(access_token, cls.jwt_secret, algorithms=[cls.jwt_algorithm])["user_id"]
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
