from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session

from app.auth import app, get_current_user
from app.database import engine, get_database
from app.exceptions import NotFoundException, UnauthorizedException
from app.models import Base
from app.models import Todo as TodoModel
from app.schemas import Todo as TodoSchema

# app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/user/todo")
async def read_all_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_database)):
    if user is None:
        raise UnauthorizedException
    return db.query(TodoModel).filter(TodoModel.owner_id == user.get("id")).all()


@app.get("/user/todo/{todo_id}")
async def read_todo_by_user(
    todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_database)
):
    if user is None:
        raise UnauthorizedException

    todo_model = db.query(TodoModel).filter(TodoModel.owner_id == user.get("id"), TodoModel.id == todo_id).first()
    if todo_model is None:
        raise NotFoundException

    return todo_model


@app.post("/user/todo/", status_code=201)
async def create_todo_by_user(
    todo: TodoSchema, user: dict = Depends(get_current_user), db: Session = Depends(get_database)
):
    if user is None:
        raise UnauthorizedException

    todo_model = TodoModel(**todo.dict())
    todo_model.owner_id = user.get("id")
    db.add(todo_model)
    db.commit()
    return todo_model


@app.put("/user/todo/{todo_id}")
async def update_todo_by_user(
    todo_id: int,
    todo: TodoSchema,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    if user is None:
        raise UnauthorizedException

    todo_model = db.query(TodoModel).filter(TodoModel.owner_id == user.get("id"), TodoModel.id == todo_id).first()
    if not todo_model:
        raise NotFoundException

    todo_data = todo.dict(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(todo_model, key, value)

    db.add(todo_model)
    db.commit()
    return todo_model


@app.delete("/user/todo/{todo_id}", status_code=204)
async def delete_todo_by_user(
    todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_database)
):
    if user is None:
        raise UnauthorizedException

    todo_model = db.query(TodoModel).filter(TodoModel.owner_id == user.get("id"), TodoModel.id == todo_id).first()
    if not todo_model:
        raise NotFoundException

    db.query(TodoModel).filter(TodoModel.owner_id == user.get("id"), TodoModel.id == todo_id).delete()
    db.commit()
    return {}


###################
# Unauthenticated #
###################
# @app.get("/")
# async def read_all(db: Session = Depends(get_database)):
#     return db.query(TodoModel).all()


# @app.get("/{todo_id}")
# async def read_todo(todo_id: int, db: Session = Depends(get_database)):
#     todo_model = db.query(TodoModel).filter(TodoModel.id == todo_id).first()

#     if not todo_model:
#         raise NotFoundException
#     return todo_model


# @app.post("/", status_code=201)
# async def create_todo(todo: TodoSchema, db: Session = Depends(get_database)):
#     todo_model = TodoModel(**todo.dict())
#     db.add(todo_model)
#     db.commit()
#     return todo_model


# @app.put("/{todo_id}", status_code=204)
# async def update_todo(todo_id: int, todo: TodoSchema, db: Session = Depends(get_database)):
#     todo_model = db.query(TodoModel).filter(TodoModel.id == todo_id).first()

#     if not todo_model:
#         raise NotFoundException

#     # todo_model.title = todo.title
#     # todo_model.description = todo.description
#     # todo_model.priority = todo.priority
#     # todo_model.complete = todo.complete

#     todo_data = todo.dict(exclude_unset=True)
#     for key, value in todo_data.items():
#         setattr(todo_model, key, value)

#     db.add(todo_model)
#     db.commit()
#     return todo_model


# @app.delete("/{todo_id}", status_code=204)
# async def delete_todo(todo_id: int, db: Session = Depends(get_database)):
#     todo_model = db.query(TodoModel).filter(TodoModel.id == todo_id).first()

#     if not todo_model:
#         raise NotFoundException

#     db.query(TodoModel).filter(TodoModel.id == todo_id).delete()
#     db.commit()
#     return {}
