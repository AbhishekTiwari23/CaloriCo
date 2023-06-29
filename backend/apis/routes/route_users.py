from database.repository.users import get_user_by_email,  get_user_by_username, delete_user_by_email,check_calories_goal
from database.sessions import get_db
from database.models.users import User
from pydantic import Field
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status,Query
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
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(email, db)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")

    if str(current_user.role) == "Role.user" and current_user.email == email:
        if (
            existing_user.first_name != user.first_name
            or existing_user.last_name != user.last_name
            or existing_user.username != user.username
            or existing_user.email != user.email
            or existing_user.role != user.role
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"User with username {current_user.username} is authorized to change their expected calories only"
            )
        existing_user.expected_calories = user.expected_calories
    else:
        if str(current_user.role) in ["Role.admin", "Role.userManager"] or current_user.email == email:
            check_user = db.query(User).filter((User.email == user.email) | (User.username == user.username)).first()
            if check_user and check_user != existing_user:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email {user.email} or username {user.username} already exists Please use another")

            existing_user.first_name = user.first_name.upper()
            existing_user.last_name = user.last_name.upper()
            existing_user.username = user.username.upper()
            existing_user.email = user.email.upper()
            existing_user.role = user.role.upper()
            existing_user.expected_calories = user.expected_calories
        db.commit()
        db.refresh(existing_user)
        json_compatabile_user = jsonable_encoder(existing_user)
        return JSONResponse(content=json_compatabile_user)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with username {current_user.username} is not authorized to access this resource {current_user.role}")

# Get all users - Working
page = Page.with_custom_options(
    size=Field(100, ge=1, le=100),
)
@user_router.get("/{role}/all", response_model=page[ShowUser])
def get_all_users(
    role: str,
    query: str = Query(None, description="Filtering by name"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if str(current_user.role) in ["Role.admin", "Role.userManager"]:
        users_query = db.query(User).filter(User.role == role)

        if query:
            users_query = users_query.filter(User.username.ilike(f"%{query}%"))

        users = users_query.all()
        paginated_users = paginate(users)
        json_compatible_users = jsonable_encoder(paginated_users.items)
        return JSONResponse(content=json_compatible_users)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"User with username {current_user.username} is not authorized to access this resource {current_user.role}"
    )


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
        total_calories = check_calories_goal(user, db)
        message = ""
        if total_calories > user.expected_calories:
            message = f"You exceeded your daily calories goal by {total_calories - user.expected_calories} calories , your total calories for today is {total_calories} and your daily goal is {user.expected_calories}"
        else:
            message = f"You did not exceed your daily calories goal by {user.expected_calories - total_calories} calories, your total calories for today is {total_calories} and your daily goal is {user.expected_calories}"
        json_compatabile_message = jsonable_encoder({"detail": message})
        return JSONResponse(content=json_compatabile_message)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with username {current_user.username} is not authorized to access this resource {current_user.role}")
