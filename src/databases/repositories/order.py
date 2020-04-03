from ._base import CRUD
from ..models import OrderSchema


class OrderRepository(CRUD):
    def __init__(self, session):
        self.session = session
        self.model = OrderSchema
