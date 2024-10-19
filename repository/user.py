from sqlalchemy.orm import Session
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

# Create an access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Authenticate user credentials
def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if user and verify_password(password, user.password_hash):  # Ensure `password_hash` exists
        return user
    return None

# Utility to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Utility to hash password
def hash_password(password):
    return pwd_context.hash(password)

def get_user_by_email_or_username(db: Session, username: str, email: str):
    statement = select(User).where(or_(User.username == username, User.email == email))
    result = db.execute(statement).first()  # Use 'execute' instead of 'exec'
    return result

# Create a new user
def create_user(db: Session, username: str, email: str, password: str):
    # Check if a user with the same email or username exists
    existing_user = get_user_by_email_or_username(db, username, email)
    if existing_user:
        if existing_user.username == username:
            raise HTTPException(status_code=400, detail="Username is already taken")
        if existing_user.email == email:
            raise HTTPException(status_code=400, detail="Email is already registered")
    
    # If no existing user, proceed to create the new user
    hashed_password = hash_password(password)
    user = User(username=username, email=email, password_hash=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str):
    statement = select(User).where(User.username == username)
    result = db.execute(statement).scalars().first()  # This returns the actual User object
    return result
