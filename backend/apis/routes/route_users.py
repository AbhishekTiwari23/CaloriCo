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
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.users import Role

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
    if str(current_user.role) in ["Role.admin", "Role.userManager"] or (current_user.username == username):
        json_compatabile_user = jsonable_encoder(user)
        return JSONResponse(content=json_compatabile_user)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with username {current_user.username} is not authorized to access this resource. Your Role: {current_user.role}")

# Route to get User By Email - Working
@user_router.get("Email/{email}", response_model=ShowUser)
def get_user_email(
    email: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with email {email} not found")
    if str(current_user.role)  in ["Role.admin", "Role.userManager"] or (current_user.email == email):
        json_compatabile_user = jsonable_encoder(user)
        return JSONResponse(content=json_compatabile_user)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with username {current_user.username} is not authorized to access this resource {current_user.role}")

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
    if str(current_user.role) in ["Role.admin", "Role.userManager"] or (current_user.email == email):
        delete_user_by_email(email, db)
        json_compatabile_message = jsonable_encoder({"detail": "User deleted successfully"})
        return JSONResponse(content=json_compatabile_message)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with username {current_user.username} is not authorized to access this resource {current_user.role}")

# Update a user by email
@user_router.put("/update/{email}", response_model=ShowUser)
def update_user(
    email: str,
    user: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    existing_user = get_user_by_email(email, db)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")
    if str(current_user.role) in ["Role.admin", "Role.userManager"] or (current_user.email == email):
        # Update the user's attributes
        existing_user.first_name = user.first_name
        existing_user.last_name = user.last_name
        existing_user.username = user.username
        existing_user.email = user.email
        existing_user.role = user.role
        existing_user.expected_calories = user.expected_calories

        db.commit()
        db.refresh(existing_user)
        json_compatabile_user = jsonable_encoder(existing_user)
        return JSONResponse(content=json_compatabile_user)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with username {current_user.username} is not authorized to access this resource {current_user.role}")


# Get all users - Working
page = Page.with_custom_options(
    size=Field(100, ge=1, le=500),
    )
@user_router.get("/{role}/all", response_model=page[ShowUser])
def get_all_users(
    role: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    if str(current_user.role) in ["Role.admin", "Role.userManager"]:
        users = db.query(User).filter(User.role == role).all()
        json_compatabile_users = jsonable_encoder(users)
        return JSONResponse(content=json_compatabile_users)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with username {current_user.username} is not authorized to access this resource {current_user.role}")

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
    if str(current_user.role) in ["Role.admin", "Role.userManager"] or (current_user.username == username):
        message = check_calories_goal(user, db)
        json_compatabile_message = jsonable_encoder({"detail": message})
        return JSONResponse(content=json_compatabile_message)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with username {current_user.username} is not authorized to access this resource {current_user.role}")
