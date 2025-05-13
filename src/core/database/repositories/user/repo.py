from typing import Optional

from core.entities import User
from core.database.database import Database
from core.database.repositories.user.repo_interface import IUserRepo


class UserRepo(IUserRepo):
    def __init__(self, db: Database):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        user = self.db.get_item({"email": email})
        if user:
            return User(**user)
        return None

    def create_user(self, user: User) -> bool:
        """Create a new user"""
        try:
            self.db.put_item(user.model_dump())
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
