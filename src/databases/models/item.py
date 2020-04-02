from sqlalchemy import Integer, String, Column, BigInteger
from .common.date_timestamp import DateTimestamp
from .base import DeclarativeBase, Base


class ItemSchema(DeclarativeBase, Base, DateTimestamp):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    pancake_id = Column(BigInteger, nullable=False, unique=True)
    pancake_order_id = Column(BigInteger, nullable=False)
    name = Column(String, nullable=False)
    variant = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
