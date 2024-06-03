from typing import Optional
from pydantic import BaseModel

from app.src.base import exceptions


class BaseGood(BaseModel):
    headline: str
    author: str
    num_of_views: int
    position: int


class GoodCreate(BaseGood):
    pass


class GoodInDB(BaseGood):
    id: int


class GoodUpdate(BaseModel):
    headline: Optional[str] = None
    author: Optional[str] = None
    num_of_views: Optional[int] = None
    position: Optional[int] = None
