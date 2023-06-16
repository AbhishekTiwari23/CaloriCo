from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from core.config import settings

from database.sessions import get_db
from database.repository.users import get_user_by_username
from schemas.token import Token
from core.hashing import Hash
from core.security import create_access_token


login_router = APIRouter()

def authenticate_user(username: str, password: str,db: Session):
    user = get_user_by_username(username=username,db=db)
    print(user)
    if not user:
        return False
    if not Hash.verify( password,user.password) :
        return False
    return user

@login_router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session= Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer",}

