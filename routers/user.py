from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from repository import user as user_repository
from dependencies import create_access_token, verify_token, get_db
from pydantic import BaseModel
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

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

# User login and token generation
@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = user_repository.authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Create a JWT token for the authenticated user
    access_token_expires = timedelta(minutes=30)
    access_token = user_repository.create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_repository.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", dependencies=[Depends(verify_token)])
def read_users_me(current_user: str = Depends(verify_token)):
    return {"user": current_user}