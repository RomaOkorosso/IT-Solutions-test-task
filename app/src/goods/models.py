from app.src.base import Base
from sqlalchemy import Column, Integer, Text


class Good(Base):
    __tablename__ = "goods"

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(Text)
    author = Column(Text)
    num_of_views = Column(Integer)
    position = Column(Integer)
