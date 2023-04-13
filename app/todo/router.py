from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.router import get_current_user
from app.database import get_database
from app.exceptions import NotFoundException, UnauthorizedException
from app.models import Base
from app.models import Todo as TodoModel
from app.todo.schemas import Todo as TodoSchema

router = APIRouter(prefix="/todo", tags=["todo"])


@router.get("/")
async def read_all_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_database)):
    if user is None:
        raise UnauthorizedException
    return db.query(TodoModel).filter(TodoModel.owner_id == user.get("id")).all()


@router.get("/{todo_id}")
async def read_todo_by_user(
    todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_database)
):
    if user is None:
        raise UnauthorizedException

    todo_model = db.query(TodoModel).filter(TodoModel.owner_id == user.get("id"), TodoModel.id == todo_id).first()
    if todo_model is None:
        raise NotFoundException

    return todo_model


@router.post("/", status_code=201)
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


@router.put("/{todo_id}")
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


@router.delete("/{todo_id}", status_code=204)
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
