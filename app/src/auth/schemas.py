import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, EmailStr

from app.src.base import exceptions


class BaseUser(BaseModel):
    full_name: str
    email: EmailStr
    username: str


class UserCreate(BaseUser):
    password: str

    @field_validator(
        "password"
    )  # validate password with regex and return it or raise an error
    def hash_password(cls, v):
        password_pattern = (
            r"^(?:(?:(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]))|(?:(?=.*[a-z])(?=.*[A-Z])(?=.*[*.!@$%^&(){}["  # noqa
            "]:;<>,.?/~_+-=|\]))|(?:(?=.*[0-9])(?=.*[A-Z])(?=.*[*.!@$%^&(){}[]:;<>,.?/~_+-=|\]))|(?:("  # noqa
            "?=.*[0-9])(?=.*[a-z])(?=.*[*.!@$%^&(){}[]:;<>,.?/~_+-=|\]))).{8,32}$"  # noqa
        )
        match_pwd = re.compile(password_pattern)

        if len(v) < 8:
            raise exceptions.WeakPassword("password must be at least 8 characters")
        if not re.fullmatch(match_pwd, v):
            raise exceptions.WeakPassword("weak password")
        return v


class UserUpdate(BaseModel):
    full_name: Optional[str]
    email: Optional[str]


class UserInDB(BaseUser):
    created_at: datetime
    updated_at: datetime


class TokenBase(BaseModel):
    access_token: str
    token_type: str
    expire_at: Optional[datetime] = None


class TokenCreate(TokenBase):
    pass


class TokenUpdate(TokenBase):
    pass


class TokenData(BaseModel):
    username: Optional[str] = None
    access_token: Optional[str] = None
