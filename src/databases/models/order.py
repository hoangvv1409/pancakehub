from sqlalchemy import (
    Integer, String, Column,
    BigInteger, DateTime,
)
from .common.date_timestamp import DateTimestamp
from .base import DeclarativeBase, Base


class OrderSchema(DeclarativeBase, Base, DateTimestamp):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    pancake_id = Column(BigInteger, nullable=False, unique=True)
    pancake_shop_id = Column(BigInteger, nullable=False)
    display_id = Column(BigInteger, nullable=False)
    fb_page_id = Column(BigInteger, nullable=True)
    inserted_at = Column(DateTime(timezone=True), nullable=True)
    order_id = Column(String, nullable=True)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    full_address = Column(String, nullable=False)
    city = Column(String, nullable=True)
    province_id = Column(Integer, nullable=False)
    district_id = Column(Integer, nullable=False)
    total_cod = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    status_str = Column(String, nullable=True)
    partner_id = Column(Integer, nullable=True)
    partner_str = Column(String, nullable=True)
    status_updated_at = Column(DateTime(timezone=True), nullable=True)
    sale = Column(String, nullable=True)
    tracking_numbers = Column(String, nullable=True)

    request_fulfilled_at = Column(DateTime(timezone=True), nullable=True)
    pick_money = Column(Integer, nullable=True)
    ship_money = Column(Integer, nullable=True)
    deliver_status = Column(String, nullable=True)
    is_freeship = Column(Integer, nullable=True)
