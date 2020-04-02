from sqlalchemy import Integer, String, Column, BigInteger, DateTime
from .common.date_timestamp import DateTimestamp
from .base import DeclarativeBase, Base


class OrderSchema(DeclarativeBase, Base, DateTimestamp):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    pancake_id = Column(BigInteger, nullable=False, unique=True)
    pancake_shop_id = Column(BigInteger, nullable=False)
    fb_page_id = Column(BigInteger, nullable=False)
    inserted_at = Column(DateTime(timezone=True), nullable=True)
    name = Column(String, nullable=False)
    order_id = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    full_address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    total_cod = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    status_str = Column(String, nullable=True)
    partner_id = Column(Integer, nullable=False)
    partner_str = Column(String, nullable=True)
    status_updated_at = Column(DateTime(timezone=True), nullable=True)
    sale = Column(String, nullable=False)
    tracking_numbers = Column(String, nullable=True)
