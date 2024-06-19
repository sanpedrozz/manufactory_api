from sqlalchemy import Column, Text, BigInteger, Boolean

from src.db.base import Base


class AlarmMessages(Base):
    __tablename__ = "alarm_messages"
    id = Column(BigInteger, primary_key=True)
    message = Column(Text, nullable=True)
    tag = Column(Text, nullable=True)
    camera = Column(Boolean, default=False, nullable=False)