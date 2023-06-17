from database.repository.users import get_user_by_email,  get_user_by_username, delete_user_by_email,check_calories_goal
from database.sessions import get_db
from database.models.users import User
from pydantic import Field
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page,paginate

from sqlalchemy.orm import Session
from schemas.users import UserCreate, ShowUser
from core.security import get_current_user

user_router = APIRouter()


# Route to get User By Username - Working
@user_router.get("/username/{username}", response_model=ShowUser)
def get_user_username(
    username: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    user = get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username {username} not found")
    if current_user.role in ["Role.admin", "Role.userManager"] or (current_user.username == username):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with username {current_user.username} is not authorized to access this resource {current_user.role}")
    return user

# Route to get User By Email - Working
@user_router.get("Email/{email}", response_model=ShowUser)
def get_user_email(
    email: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    user = get_user_by_email(email, db)
    if current_user.role in ["Role.admin", "Role.userManager"] or (current_user.email == email):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with username {current_user.username} is not authorized to access this resource {current_user.role}")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with email {email} not found")
    return user

# Route to delete a user by email - Working
@user_router.delete("Email/{email}")
def delete_user_email(
    email: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with email {email} not found")
    if current_user.role in ["Role.admin", "Role.userManager"] or (current_user.email == email):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with username {current_user.username} is not authorized to access this resource {current_user.role}")
    delete_user_by_email(email, db)
    return {"detail": "User deleted successfully"}

# Update a user by email - Working
@user_router.put("/update/{email}", response_model=ShowUser)
def update_user(
    email: str,
    user: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    existing_user = get_user_by_email(email, db)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")
    if current_user.role in ["Role.admin", "Role.userManager"] or (current_user.email == email):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with username {current_user.username} is not authorized to access this resource {current_user.role}")

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
page = Page.with_custom_options(
    size=Field(100, ge=1, le=500),
    )
@user_router.get("/{role}/all", response_model=page[ShowUser])
def get_all_users(
    role: str,
    # current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    # if current_user.role not in ["Role.admin", "Role.userManager"]:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with username {current_user.username} is not authorized to access this resource {current_user.role}")
    users = db.query(User).filter(User.role == role).all()
    return paginate(users)

#  Check calories - Working
@user_router.get("/target_calories/{username}", response_model=str)
def check_calories(
    username: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    user = get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with username {username} not found")
    if current_user.role in ["Role.admin", "Role.userManager"] or (current_user.username == username):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with username {current_user.username} is not authorized to access this resource {current_user.role}")
    message = check_calories_goal(user, db)
    return message
