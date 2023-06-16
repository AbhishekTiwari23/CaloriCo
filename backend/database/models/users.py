from sqlalchemy import Column, Date, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from database.baseClass import Base
from schemas.users import Role

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    join_date = Column(Date)
    role = Column(Enum(Role), default="user")
    expected_calories = Column(Integer)

    food = relationship("Food", back_populates="owner")


