from fastapi import FastAPI
from core.config import settings
from database.sessions import engine, SessionLocal
from database.baseClass import Base

from apis.routes import route_users, route_food, route_login



def include_router(app):
    app.include_router(route_users.user_router, tags=["Users"], prefix="/users")
    app.include_router(route_food.food_router, tags=["Food"], prefix="/food")
    app.include_router(route_login.login_router, tags=["Login"], prefix="/login")   

def configure_database(app):
    Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    include_router(app)
    configure_database(app)
    return app

app = start_application()
