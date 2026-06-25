from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String


class Base(DeclarativeBase):
    pass


class Url(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    long_url = Column(String, unique=True)
    short_code = Column(String, unique=True)
    click_count = Column(Integer, default=0)