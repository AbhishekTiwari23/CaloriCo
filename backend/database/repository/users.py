from sqlalchemy.orm import Session
from datetime import datetime
from database.models.users import User
from schemas.users import UserCreate
from fastapi import HTTPException, status
from core.hashing import Hash
from database.models.food import Food

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
        total_calories += (food.calories)
    if total_calories > user.expected_calories:
        return f"You exceeded your daily calories goal by {total_calories - user.expected_calories} calories , your total calories for today is {total_calories} and your daily goal is {user.expected_calories}"
    else:
        return f"You did not exceed your daily calories goal by {user.expected_calories - total_calories} calories, your total calories for today is {total_calories} and your daily goal is {user.expected_calories}"