from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import select

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, name: str, age: int):
        user = User(name=name,age=age)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_all(self):
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def get_by_id(self, user_id: int):
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()