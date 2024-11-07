from sqlalchemy import Column, BigInteger, Integer, String, Double, ForeignKey
from sqlalchemy.orm import declarative_base

# Настройка базы для моделей SQLAlchemy
Base = declarative_base()


# Определение модели Item
class Item(Base):
    __tablename__ = 'items'
    id = Column(BigInteger, primary_key=True)
    label_id = Column(BigInteger, unique=True, nullable=False)
    edge_length_1 = Column(Double)
    edge_length_2 = Column(Double)
    edge_width_3 = Column(Double)
    edge_width_4 = Column(Double)
    plan_set_id = Column(String)
    history_object_id = Column(BigInteger, ForeignKey('industry_operations_history.object_id'))


# Определение модели IndustryOperationsHistory
class IndustryOperationsHistory(Base):
    __tablename__ = 'industry_operations_history'
    id = Column(BigInteger, primary_key=True)
    object_id = Column(BigInteger, nullable=False)
    operation_id = Column(Integer, nullable=False)
    operation_property1 = Column(Integer)
