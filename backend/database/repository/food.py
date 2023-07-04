from sqlalchemy.orm import Session
from database.models.food import Food
from database.models.users import User
from schemas.food import FoodCreate
from datetime import datetime,date
from core.calories import get_calories
import json
from fastapi import HTTPException, status

def create_new_food(user:User,food: FoodCreate, db: Session):

    add_date = food.date
    if not food.date:
        add_date = date.today()
    
    add_calories = food.calories

    if food.name:
        api_response = get_calories(food.name.upper(), food.quantity)
        data = json.loads(api_response)
        if data['items'] == []:
            raise HTTPException(status_code=403,detail=f"Invalid food name,")
        if not food.calories:
            add_calories = data['items'][0]['calories']

    if(food.quantity <=0 ):
        raise HTTPException(status_code=403,detail=f"Quantity must be a positive integer")

    food_exist = db.query(Food).filter(Food.owner_id == user.id,Food.name == food.name.upper(),Food.date == date.today()).first()

    if food_exist:
        food_exist.quantity += food.quantity
        api_response = get_calories(food.name.upper(), food.quantity)
        data = json.loads(api_response)
        food_exist.calories += data['items'][0]['calories']
        db.commit()
        db.refresh(food_exist)
        return food_exist
    else:
        new_food = Food(
            name=food.name.upper(),
            date=add_date,
            time = food.time,
            quantity=food.quantity or 1,
            calories=add_calories,
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
    if food.owner_id == user.id or str(user.role) in ["Role.admin", "Role.userManager"] :
        db.query(Food).filter(Food.id == food_id).delete()
        db.commit()
        return {"message": f"Food deleted successfully for {user.username} and id {food_id}"}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User not authorized to update this food")