from app.schemas.user import UserCreate
from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, user: UserCreate):
        return await self.repo.create(user.name, user.age)
    
    async def get_users(self):
        return await self.repo.get_all()

    async def get_user(self, user_id: int):
        return await self.repo.get_by_id(user_id)