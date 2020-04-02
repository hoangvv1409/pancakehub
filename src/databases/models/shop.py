from sqlalchemy import Integer, String, Column, JSON, BigInteger
from .common.date_timestamp import DateTimestamp
from .base import DeclarativeBase, Base


class ShopSchema(DeclarativeBase, Base, DateTimestamp):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True)
    pancake_id = Column(BigInteger, nullable=False, unique=True)
    name = Column(String, nullable=False)
    info = Column(JSON, nullable=True)
