from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

def get_user_service(db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)

@router.post("")
async def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.create_user(user)

@router.get("")
async def get_users(
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_users()

@router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
    return current_user
    
@router.get("/{user_id}")
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user(user_id)
