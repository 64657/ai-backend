from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app.models.user import User
from fastapi import HTTPException, status

class AuthService:
    def __init__(self, repo):
        self.repo = repo

    async def register(self, user):
        existing = await self.repo.get_by_email(user.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        hashed = hash_password(user.password)

        return await self.repo.create(
            name=user.name,
            email=user.email,
            hashed_password=hashed
        )

    async def login(self, user):
        db_user = await self.repo.get_by_email(user.email)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        token = create_access_token({"sub": db_user.email})

        return {
            "access_token": token,
            "token_type": "bearer"
        }