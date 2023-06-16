from database.repository.users import create_new_user, get_user_by_email,  get_user_by_username, delete_user_by_email
from database.sessions import get_db

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from schemas.users import UserCreate, ShowUser

user_router = APIRouter()


# Route to create a new user - Working
@user_router.post("/",response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user, db)
    return user


# Route to get User By Username - Working
@user_router.get("Username/{username}", response_model=ShowUser)
def get_user_username(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with username {username} not found")
    return user

# Route to get User By Email - Working
@user_router.get("Email/{email}", response_model=ShowUser)
def get_user_email(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with email {email} not found")
    return user

# Route to delete a user by email - Working
@user_router.delete("Email/{email}")
def delete_user_email(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with email {email} not found")
    delete_user_by_email(email, db)
    return {"detail": "User deleted successfully"}