from ._base import CRUD
from ..models import RawOrderSchema


class RawOrderRepository(CRUD):
    def __init__(self, session):
        self.session = session
        self.model = RawOrderSchema
