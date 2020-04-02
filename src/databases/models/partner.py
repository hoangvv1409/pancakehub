from sqlalchemy import Integer, String, Column
from .common.date_timestamp import DateTimestamp
from .base import DeclarativeBase, Base


class PartnerSchema(DeclarativeBase, Base, DateTimestamp):
    __tablename__ = 'partners'

    id = Column(Integer, primary_key=True)
    pancake_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
