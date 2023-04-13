from typing import Optional, Any, Dict
from fastapi import HTTPException


class HTTPBaseException(HTTPException):
    def __init__(self, headers: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail, headers=headers)


class NotFoundException(HTTPBaseException):
    status_code = 404
    detail = "Not Found"


class UnauthorizedException(HTTPBaseException):
    status_code = 401
    detail = "Not authorized for this operation"
