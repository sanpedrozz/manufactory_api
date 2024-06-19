# src/db/model.py

from typing import TypeVar, List
#from src.db.model import OperationHistory

T = TypeVar("T")


class BaseRepo():
    model: type[T]


#     @classmethod
#     async def get_place_by_id(cls, db: AsyncSession, row_id: int) -> type[T]:
#         """
#         Get a record by ID.
#         :param db: The database session.
#         :param row_id: The ID .
#         :return: The record.
#         """
#         try:
#             stmt = select(cls).filter(cls.model.id == row_id)
#             result = await db.execute(stmt)
#             record = result.scalars().first()
#
#             if not record:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND,
#                     detail=f"Place with id {row_id} not found"
#                 )
#
#             return record
#         except SQLAlchemyError as ex:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=str(ex)
#             ) from ex
#
#     @classmethod
#     async def get_all(cls, db: AsyncSession, limit: int | None = None) -> List[type[T]]:
#         """
#         Get all records.
#         :param db: The database session.
#         :return: A list of all records.
#         """
#         try:
#             if limit:
#                 stmt = select(cls.model).limit(limit)
#             else:
#                 stmt = select(cls.model)
#             result = await db.execute(stmt)
#             return list(result.scalars().all())
#         except SQLAlchemyError as ex:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=str(ex)
#             ) from ex
#
# class OperationHistoryRepo(BaseRepo):
#     model = OperationHistory