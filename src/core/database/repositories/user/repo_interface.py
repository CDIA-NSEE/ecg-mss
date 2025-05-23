from abc import abstractmethod
from typing import Optional

from core.entities import User


class IUserRepo:
    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass

    @abstractmethod
    def create_user(self, user: User) -> bool:
        """Create a new user"""
        pass
