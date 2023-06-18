from pydantic import BaseModel, Field, validator
from datetime import datetime, date, time
from typing import Optional

add_time = datetime.utcnow().time().strftime("%H:%M:%S")

class FoodCreate(BaseModel):
    name: str = Field(example="apple", description="Name of the food")
    date: date
    time : str = Field(example=add_time, description="Time of the food")
    quantity: int = Field(example=1, description="Quantity of the food")
    calories: Optional[str] = Field(example="95", description="Calories of the food")

    @validator('time', pre=True)
    def validate_time(cls, value):
        try:
            return str(datetime.strptime(value, '%H:%M:%S'))
        except ValueError:
            raise ValueError('Invalid time format. Please use the format HH:MM:SS')


    class Config:
        orm_mode = True

class ShowFood(BaseModel):
    name: str = Field(description="Name of the food")
    date: date
    time : str = Field(description="Time of the food")
    quantity: int = Field(description="Quantity of the food")
    calories: Optional[str] = Field(description="Calories of the food")
    owner_id: int = Field(description="ID of the food owner")



    class Config:
        orm_mode = True