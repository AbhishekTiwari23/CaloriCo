from sqlalchemy.orm import Session
from database.models.food import Food
from database.models.users import User
from schemas.food import FoodCreate
from datetime import datetime
from core.calories import get_calories
import json
from fastapi import HTTPException, status

def create_new_food(user:User,food: FoodCreate, db: Session):

    add_date = food.date or datetime.utcnow().date()
    # add_time = food.time or datetime.utcnow().strftime("%H:%M:%S")
    add_calories = food.calories
    if not food.calories:
        try:
            api_response = get_calories(food.name, food.quantity)
            data = json.loads(api_response)
            add_calories = data['items'][0]['calories']
        except:
            raise HTTPException(status_code=403,detail="Invalid food name")
    if(food.quantity <=0 ):
        raise HTTPException(status_code=403,detail="Quantity must be a positive integer")
    new_food = Food(
        name=food.name,
        date=add_date,
        # time = add_time,
        quantity=food.quantity or 1,
        calories=add_calories,
        owner_id=user.id
    )

    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return new_food

# def get_user_food_by_username(username: str, db: Session):
#     user = db.query(User).filter(User.username == username).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with username {username} not found")
#     user_food = db.query(Food).filter(Food.owner_id == user.id).all()
#     return user_food
