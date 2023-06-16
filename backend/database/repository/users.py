from sqlalchemy.orm import Session
from datetime import datetime
from database.models.users import User
from schemas.users import UserCreate
from fastapi import HTTPException, status
from core.hashing import Hash

# Create a new user - Working
def create_new_user(user: UserCreate, db: Session):
    # Check if the email already exists
    existing_user = db.query(User).filter((User.email == user.email)|(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"User with email {user.email} or username {user.username} already exists")
    join_date = user.join_date or datetime.now()
    expected_calories = user.expected_calories or 2200

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password = Hash.bcrypt(user.password),
        join_date=join_date,
        role=user.role,
        expected_calories=expected_calories,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get a user by email - Working
def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user

# Get a user by username
def get_user_by_username(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    return user

