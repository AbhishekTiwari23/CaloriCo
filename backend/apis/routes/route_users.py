from database.repository.users import create_new_user, get_user_by_email,  get_user_by_username, delete_user_by_email
from database.sessions import get_db
from database.models.users import User

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from schemas.users import UserCreate, ShowUser,Role

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

# Update a user by email - Working
@user_router.put("/update/{email}", response_model=ShowUser)
def update_user(email: str, user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(email, db)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")

    # Update the user's attributes
    existing_user.first_name = user.first_name
    existing_user.last_name = user.last_name
    existing_user.username = user.username
    existing_user.email = user.email
    existing_user.role = user.role
    existing_user.expected_calories = user.expected_calories

    db.commit()
    db.refresh(existing_user)
    return existing_user

# Get all users - Working
@user_router.get("/{role}/all", response_model=list[ShowUser])
def get_all_users(role: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.role == role).all()
    return users
