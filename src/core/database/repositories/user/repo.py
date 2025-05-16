from typing import Optional

from core.entities import User
from core.database.database import Database
from core.database.repositories.user.repo_interface import IUserRepo


class UserRepo(IUserRepo):
    def __init__(self, db: Database):
        self.table = db.table

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        user = self.table.get_item(
            Key={
                "PK": f"USER#{email}"
            }
        )
        if user:
            return User.from_dynamo(user)
        return None

    def create_user(self, user: User) -> bool:
        """Create a new user"""
        try:
            self.table.put_item(user.to_dynamo())
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
