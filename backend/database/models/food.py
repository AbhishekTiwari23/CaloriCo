from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time
from sqlalchemy.orm import relationship
from datetime import date
from database.baseClass import Base

class Food(Base):
    __tablename__ = "food"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    date = Column(String, default=date.today())
    time = Column(String)
    quantity = Column(Integer, default=1)
    calories = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="food")