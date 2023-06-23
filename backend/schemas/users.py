from pydantic import BaseModel, EmailStr, Field
from datetime import date
from enum import Enum

class Role(str, Enum):
    user = "USER"
    userManager = "USERMANAGER"
    admin = "ADMIN"

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    first_name: str = Field(example="John")
    last_name: str = Field(example="Doe")
    username: str = Field(example="johndoe")
    email: EmailStr = Field(example="john@gmail.com")
    password: str = Field(example="password")
    join_date: date = Field(example=date.today())
    role: Role = "user"
    expected_calories: int = Field(example=2000)

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    join_date: date
    role: str
    expected_calories: int

    class Config:
        orm_mode = True

class UsersList(BaseModel):
    users: list[ShowUser]

    class Config:
        orm_mode = True

