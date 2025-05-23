from decimal import Decimal

from pytz import UTC
from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str
    created_at: datetime = datetime.now(UTC)

    def to_dynamo(self):
        return {
            "PK": f"USER#{self.email}",
            "SK": Decimal(self.created_at.timestamp()),
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }

    @classmethod
    def from_dynamo(cls, data: dict) -> "User":
        return cls(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            created_at=datetime.fromtimestamp(float(data["SK"]), tz=UTC),
        )
