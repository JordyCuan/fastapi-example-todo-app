from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, get_database
from .exceptions import NotFoundException
from .models import Base, User

SECRET_KEY = "lhgGHo7t8O7Ff68OF688o68O6F6fF68O"
ALGORITHM = "HS256"

oauth_bearer = OAuth2PasswordBearer(tokenUrl="token")


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    firstname: str
    lastname: str
    password: str


app = FastAPI()
bcript_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return bcript_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcript_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user: User = db.query(User).filter(User.username == username).first()

    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    now = datetime.utcnow()

    expire = now + timedelta(minutes=15)
    if expires_delta:
        expire = now + expires_delta

    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        if username is None or user_id is None:
            raise NotFoundException  # TODO - Unauthorized?
        return {"username": username, "id": user_id}
    except JWTError as exc:
        raise NotFoundException from exc


@app.post("/create/user", status_code=201)
async def create_new_user(user: CreateUser, db: Session = Depends(get_database)):
    user_model = User(**user.dict())
    user_model.password = get_password_hash(user_model.password)

    db.add(user_model)
    db.commit()
    return {}


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_database)
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise NotFoundException

    token = create_access_token(user.username, user.id)
    # More: https://stackoverflow.com/questions/59808854/swagger-authorization-bearer-not-send
    return {"access_token": token, "token_type": "bearer"}
