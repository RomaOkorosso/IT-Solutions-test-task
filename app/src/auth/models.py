from datetime import datetime, timedelta

from app.src.base import Base, settings
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from logger import logger


def get_expire_datetime() -> datetime:
    expire_at = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    logger.log(f"{datetime.now()} - get expire datetime for token {expire_at}")
    return expire_at


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(Text)
    email = Column(Text)
    username = Column(Text)
    password = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tokens = relationship("Token")


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    expire_at = Column(DateTime, default=get_expire_datetime)
