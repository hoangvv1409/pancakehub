from sqlalchemy import Integer, String, Column, BigInteger
from .common.date_timestamp import DateTimestamp
from .base import DeclarativeBase, Base


class FbPageSchema(DeclarativeBase, Base, DateTimestamp):
    __tablename__ = 'fb_pages'

    id = Column(Integer, primary_key=True)
    fb_page_id = Column(BigInteger, nullable=False, unique=True)
    pancake_shop_id = Column(BigInteger, nullable=False)
    name = Column(String, nullable=False)
