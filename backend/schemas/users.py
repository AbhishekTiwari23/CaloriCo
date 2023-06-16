from pydantic import BaseModel, EmailStr
from datetime import date
from enum import Enum

class Role(str, Enum):
    user = "user"
    userManager = "userManager"
    admin = "admin"

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    join_date: date
    role: Role = "user"
    expected_calories: int

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

