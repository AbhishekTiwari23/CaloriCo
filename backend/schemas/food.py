from pydantic import BaseModel, Field
from datetime import datetime, date, time
from typing import Optional

add_time = datetime.utcnow().strftime("%H:%M:%S")

class FoodCreate(BaseModel):
    name: str = Field(example="apple", description="Name of the food")
    date: date
    time: Optional[time]
    quantity: int = Field(example=1, description="Quantity of the food")
    calories: Optional[int] = Field(example=95, description="Calories of the food")

    class Config:
        orm_mode = True

class ShowFood(BaseModel):
    name: str = Field(description="Name of the food")
    date: date
    time : time
    quantity: int = Field(description="Quantity of the food")
    calories: Optional[int] = Field(description="Calories of the food")
    owner_id: int = Field(description="ID of the food owner")

    class Config:
        orm_mode = True
