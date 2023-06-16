from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.security import get_current_user
from database.models.food import Food
from database.sessions import get_db
from schemas.food import FoodCreate, ShowFood
from database.repository.food import create_new_food,delete_food
from database.models.users import User


food_router = APIRouter()

# Route to create a new food - Working
@food_router.post("/{user_name}/new_food", response_model=ShowFood)
def create_food(user_name: str, food: FoodCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with user name {user_name} not found")

    food = create_new_food(user, food, db)
    return food

# get all food - Working
@food_router.get("/{userName}/all", response_model=list[ShowFood])
def get_all_food(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
    if existing_user.id != user.id or user.role not in ["Role.admin", "Role.userManager"] :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User not authorized to update this food")
    return db.query(Food).filter(Food.owner_id == user.id).all()

# delete food - Working
@food_router.delete("{/delete/{food_id}", response_model=dict)
def delete_user_food(food_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    message = delete_food(user, food_id, db)
    return message

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
    if existing_food.owner_id != user.id or user.role not in ["Role.admin", "Role.userManager"] :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User not authorized to update this food")
    existing_food.name = food.name
    existing_food.quantity = food.quantity
    existing_food.calories = food.calories
    db.commit()
    db.refresh(existing_food)
    return existing_food
