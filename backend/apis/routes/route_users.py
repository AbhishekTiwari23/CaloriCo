from database.repository.users import create_new_user
from database.sessions import get_db

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from schemas.users import UserCreate

user_router = APIRouter()


# Route to create a new user - Working
@user_router.post("/",response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user, db)
    return user
