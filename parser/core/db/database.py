from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from settings import settings

engine = create_engine(settings.db.url)
session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)