from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Register a new user",
    description="Create a new account with an email and password. Passwords are hashed before storage.",
)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user account."""
    return await register_user(db, user_data)


@router.post(
    "/login",
    summary="Log in and receive a JWT token",
    description="Authenticate an existing user and return a bearer access token for protected routes.",
)
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Authenticate a user and return a JWT access token."""
    return await login_user(db, login_data)