from datetime import datetime

from sqlalchemy import Column, ForeignKey, Text, Integer, BigInteger, DateTime, String
from sqlalchemy.orm import relationship

from shared.db.base import Base


class OperationHistory(Base):
    __tablename__ = "operations_history"
    id = Column(BigInteger, primary_key=True)
    place_id = Column(Integer, ForeignKey('places.id'))
    program = Column(Text)
    text = Column(Text)
    dt_created = Column(DateTime, default=datetime.now)

    place = relationship("Place", back_populates="operations")


class Place(Base):
    __tablename__ = "places"
    id = Column(BigInteger, primary_key=True)
    name = Column(Text)
    message_thread_id = Column(String, default="General", nullable=False)
    ip = Column(String(45), nullable=True)

    operations = relationship("OperationHistory", back_populates="place", post_update=True)
    alarm_histories = relationship("AlarmHistory", back_populates="place", post_update=True)


class AlarmMessages(Base):
    __tablename__ = "alarm_messages"
    id = Column(BigInteger, primary_key=True)
    message = Column(Text, nullable=True)
    tag = Column(Text, nullable=True)

    alarm_histories = relationship("AlarmHistory", back_populates="alarm", post_update=True)  # Добавлено


class AlarmHistory(Base):
    __tablename__ = "alarm_history"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    place_id = Column(BigInteger, ForeignKey('places.id'), nullable=False)
    alarm_id = Column(BigInteger, ForeignKey('alarm_messages.id'), nullable=False)
    comments = Column(Text, nullable=True)
    dt_created = Column(DateTime, default=datetime.now, nullable=False)

    place = relationship("Place", back_populates="alarm_histories")
    alarm = relationship("AlarmMessages", back_populates="alarm_histories")


class PLCData(Base):
    __tablename__ = "plc_data"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    dt_created = Column(DateTime, default=datetime.now, nullable=False)
    name = Column(String, nullable=False)  # Имя переменной
    value = Column(Text, nullable=False)  # Значение переменной в строковом формате
