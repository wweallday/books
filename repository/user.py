from sqlalchemy.ext.asyncio import AsyncSession
from models.model import User
from passlib.context import CryptContext
from sqlmodel import select
from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta
from config import settings
from sqlalchemy import or_

# For hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create an access token (remains the same)
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Authenticate user credentials (async)
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if user and verify_password(password, user.password_hash):
        return user
    return None

# Utility to verify password (remains the same)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Utility to hash password (remains the same)
def hash_password(password):
    return pwd_context.hash(password)

# Get user by email or username (async)
async def get_user_by_email_or_username(db: AsyncSession, username: str, email: str):
    statement = select(User).where(or_(User.username == username, User.email == email))
    result = await db.execute(statement)  # Await the async execution
    return result.scalars().first()

# Create a new user (async)
async def create_user(db: AsyncSession, username: str, email: str, password: str):
    # Check if a user with the same email or username exists
    existing_user = await get_user_by_email_or_username(db, username, email)
    if existing_user:
        if existing_user.username == username:
            raise HTTPException(status_code=400, detail="Username is already taken")
        if existing_user.email == email:
            raise HTTPException(status_code=400, detail="Email is already registered")
    
    # If no existing user, proceed to create the new user
    hashed_password = hash_password(password)
    user = User(username=username, email=email, password_hash=hashed_password)
    db.add(user)
    await db.commit()  # Await commit for async session
    await db.refresh(user)  # Await refresh
    return user

# Get user by username (async)
async def get_user_by_username(db: AsyncSession, username: str):
    statement = select(User).where(User.username == username)
    result = await db.execute(statement)  # Await the async execution
    return result.scalars().first()
