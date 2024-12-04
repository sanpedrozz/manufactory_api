from sqlalchemy import Column, BigInteger, Integer, String, Double, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

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
    length_final = Column(Double)
    width_final = Column(Double)
    plan_set_id = Column(String)
    history_object_id = Column(BigInteger, ForeignKey('industry_operations_history.object_id'))


# Определение модели IndustryOperationsHistory
# Definition of the Place model
class Place(Base):
    __tablename__ = 'places'
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    # Other fields...


# Definition of the IndustryOperationsHistory model
class IndustryOperationsHistory(Base):
    __tablename__ = 'industry_operations_history'
    id = Column(BigInteger, primary_key=True)
    place_id = Column(BigInteger, ForeignKey('places.id', ondelete='CASCADE'), nullable=False)
    object_id = Column(BigInteger, ForeignKey('industry_operations_history_objects.id', ondelete='SET NULL'),
                       nullable=False)
    operation_id = Column(Integer, ForeignKey('operations.id'), nullable=False)
    operation_property1 = Column(Integer)
    operation_property2 = Column(Integer)
    manual = Column(Boolean, default=False, nullable=False)
    error = Column(Boolean, default=False, nullable=False)
    error_description = Column(String)
    creation_dt = Column(DateTime, default=func.now())
    employee_id = Column(Integer, ForeignKey('employees.id'))
    comment = Column(String, default="")

    # Relationship to access the place's name
    place = relationship("Place", backref="operations_history")
