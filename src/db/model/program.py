from sqlalchemy import Column, ForeignKey, Text, Integer

from src.db.base import Base


class Program(Base):
    __tablename__ = "program"
    id = Column(Integer, primary_key=True, autoincrement=True)
    program = Column(Text)
