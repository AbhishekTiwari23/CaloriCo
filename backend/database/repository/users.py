from sqlalchemy.orm import Session
from datetime import datetime
from database.models.users import User
from schemas.users import UserCreate
from fastapi import HTTPException, status
from core.hashing import Hash
from core.password import PasswordStrength
from database.models.food import Food

# Create a new user - Working
def create_new_user(user: UserCreate, db: Session):
    # Check if the email already exists
    existing_user = db.query(User).filter((User.email == user.email.upper())|(User.username == user.username.upper())).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"User with email {user.email.upper()} or username {user.username.upper()} already exists")

    # Check for password strength
    if not PasswordStrength.is_strong(user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Password is not strong enough, it must contain at least 8 characters, 1 uppercase, 1 lowercase, 1 number and 1 special character, please try again {user.username.upper()}")

    join_date = user.join_date or datetime.now()
    expected_calories = user.expected_calories or 2200

    new_user = User(
        first_name=user.first_name.upper(),
        last_name=user.last_name.upper(),
        username=user.username.upper(),
        email=user.email.upper(),
        password = Hash.bcrypt(user.password),
        join_date=join_date,
        role=user.role.upper(),
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

#  Delete a user by email
def delete_user_by_email(email: str, db: Session):
    current_user = db.query(User).filter(User.email == email)
    if not current_user.first():
        return 0
    current_user.delete(synchronize_session=False)
    db.commit()
    return 1

# Get a user by id
def get_user_by_id(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()
    return user

# Check if a user achieved his daily calories goal
def check_calories_goal(user: User, db: Session):
    total_calories = 0
    food_list = db.query(Food).filter(Food.owner_id == user.id).all()
    for food in food_list:
        if food.calories:
            total_calories += int(food.calories)
    return total_calories