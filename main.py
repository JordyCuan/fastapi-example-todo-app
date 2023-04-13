from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.database import engine
from app.models import Base
from app.todo.router import router as todo_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(todo_router)
