from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.security import get_current_user
from database.models.food import Food
from database.sessions import get_db
from schemas.food import FoodCreate, ShowFood
from database.repository.food import create_new_food
from database.models.users import User


food_router = APIRouter()

@food_router.post("/{user_id}/new_food", response_model=ShowFood)
def create_food(user_id: int, food: FoodCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")

    food = create_new_food(user, food, db)
    return food

# @food_router.put("/update/{user_id}/{food_id}", response_model=ShowFood)
# def update_food(food_id: int, food: FoodCreate, db: Session = Depends(get_db)):
#     food = db.query(Food).filter(Food.id == food_id).update(food.dict())
#     db.commit()
#     db.refresh(food)
#     return food
