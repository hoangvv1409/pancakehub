from sqlalchemy import Integer, Column, JSON, BigInteger, DateTime
from .common.date_timestamp import DateTimestamp
from .base import DeclarativeBase, Base


class RawOrderSchema(DeclarativeBase, Base, DateTimestamp):
    __tablename__ = 'raw_orders'

    id = Column(Integer, primary_key=True)
    pancake_id = Column(BigInteger, nullable=False, unique=True)
    pancake_shop_id = Column(BigInteger, nullable=False)
    payload = Column(JSON, nullable=True)
    inserted_at = Column(DateTime(timezone=True), nullable=True)
