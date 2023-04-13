from pydantic import BaseModel, Field
from typing import Optional


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(ge=1, le=5, description="Must be between 1-5")
    complete: bool
