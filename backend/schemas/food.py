from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class FoodCreate(BaseModel):
    name: str = Field(example="apple", description="Name of the food")
    date: date
    quantity: int = Field(example=1, description="Quantity of the food")
    calories: Optional[str] = Field(example="95", description="Calories of the food") 

    class Config:
        orm_mode = True

class ShowFood(BaseModel):
    name: str = Field(description="Name of the food")
    date: date
    quantity: int = Field(description="Quantity of the food")
    calories: Optional[str] = Field(description="Calories of the food")
    owner_id: int = Field(description="ID of the food owner")

    class Config:
        orm_mode = True
