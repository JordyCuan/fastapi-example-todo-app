from typing import Optional

from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    firstname: str
    lastname: str
    password: str
