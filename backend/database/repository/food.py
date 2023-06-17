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
    add_calories = food.calories
    if not food.calories:
        try:
            api_response = get_calories(food.name, food.quantity)
            data = json.loads(api_response)
            add_calories = data['items'][0]['calories']
        except:
            raise HTTPException(status_code=403,detail=f"Invalid food name,")
    if(food.quantity <=0 ):
        raise HTTPException(status_code=403,detail="Quantity must be a positive integer")
    new_food = Food(
        name=food.name,
        date=add_date,
        time = food.time or datetime.utcnow().strftime("%H:%M:%S"),
        quantity=food.quantity or 1,
        calories=int(add_calories),
        owner_id=user.id
    )

    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return new_food


def get_food_list(db: Session, user: User):
    food_list = db.query(Food).filter(Food.owner_id == user.id).all()
    return food_list

def delete_food(user:User,food_id:int, db: Session):
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Food with id {food_id} not found")
    if food.owner_id != user.id or user.role not in ["Role.admin", "Role.userManager"] :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User not authorized to update this food")
    db.query(Food).filter(Food.id == food_id).delete()
    db.commit()
    return {"message": "Food deleted successfully"}
