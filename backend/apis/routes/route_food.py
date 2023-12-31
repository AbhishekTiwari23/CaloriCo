from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy.orm import Session
from core.security import get_current_user
from database.models.food import Food
from database.sessions import get_db
from schemas.food import FoodCreate, ShowFood
from database.repository.food import create_new_food,delete_food
from database.models.users import User
from database.repository.users import get_user_by_username
from fastapi_pagination import Page, paginate
from pydantic import Field
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from database.repository.users import check_calories_goal
food_router = APIRouter()

# Route to create a new food - Working
@food_router.post("/{userName}/new_food", response_model=ShowFood)
def create_food(
    userName: str,
    food: FoodCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)):
    existing_user =get_user_by_username(userName, db)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with user name {userName} not found")
    if existing_user.id  or str(user.role) in ["Role.admin", "Role.userManager"] :
        expected_calories = check_calories_goal(existing_user, db)
        if expected_calories > existing_user.expected_calories:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Expected calories {expected_calories} is greater than user's calories goal {user.expected_calories} by {expected_calories - user.expected_calories}")
        food = create_new_food(existing_user, food, db)
        json_compatabile_food = jsonable_encoder(food)
        return JSONResponse(content=json_compatabile_food)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User not authorized to create this food")

page = Page.with_custom_options(
    size=Field(100, ge=1, le=100),
)

@food_router.get("/{userName}/all", response_model=page[ShowFood])
def get_all_food(
    userName: str,
    db: Session = Depends(get_db),
    query: str = Query(None, description="Filtering by Food name"),
    user: User = Depends(get_current_user),
):
    existing_user = get_user_by_username(userName, db)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if existing_user.id or str(user.role) in ["Role.admin", "Role.userManager"]:
        food_query = db.query(Food).filter(Food.owner_id == existing_user.id)
        if query:
            food_query = food_query.filter(Food.name.ilike(f"%{query}%"))

        query_result = food_query.all()
        json_compatabile_query = jsonable_encoder(paginate(query_result))
        return JSONResponse(content=json_compatabile_query)

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to get this data")


# delete food - Working
@food_router.delete("/delete/{userName}/{food_id}", response_model=dict)
def delete_user_food(
    userName: str,
    food_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)):

    existing_user = get_user_by_username(userName, db)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with user name {userName} not found")
    if existing_user.id or str(user.role) in ["Role.admin", "Role.userManager"]:
        message = delete_food(existing_user, food_id, db)
        json_compatabile_message = jsonable_encoder(message)
        return JSONResponse(content=json_compatabile_message)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User not authorized to delete this food")

# update food - Working
@food_router.put("/update/{food_id}", response_model=ShowFood)
def update_food(
    food_id: int,
    food: FoodCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
    existing_food = db.query(Food).filter(Food.id == food_id).first()
    if not existing_food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Food with id {food_id} not found")
    if existing_food.owner_id == user.id or str(user.role) in ["Role.admin", "Role.userManager"] :
        existing_food.name = food.name.upper()
        existing_food.quantity = food.quantity
        existing_food.calories = food.calories
        db.commit()
        db.refresh(existing_food)
        json_compatabile_food = jsonable_encoder(existing_food)
        return JSONResponse(content=json_compatabile_food)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User not authorized to update this food")