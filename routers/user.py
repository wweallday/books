from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from repository import user as user_repository
from dependencies import get_db, get_current_user
from pydantic import BaseModel
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from models.model import User, UserResponse

router = APIRouter()

# Pydantic models for request/response validation
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Register a new user
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = user_repository.create_user(db, user.username, user.email, user.password)
    return {"username": new_user.username, "email": new_user.email}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    db_user = await user_repository.authenticate_user(db, form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Create a JWT token for the authenticated user, use user.id in sub
    access_token_expires = timedelta(minutes=30)
    access_token = user_repository.create_access_token(
        data={"sub": str(db_user.id)},  # Store the user id in the sub field
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
