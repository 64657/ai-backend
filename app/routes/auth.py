from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import UserRegister, UserLogin
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_auth_service(db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    return AuthService(repo)

@router.post("/register")
async def register(user: UserRegister, service: AuthService = Depends(get_auth_service)):
    return await service.register(user)

@router.post("/login")
async def login(user: UserLogin, service: AuthService = Depends(get_auth_service)):
    return await service.login(user)