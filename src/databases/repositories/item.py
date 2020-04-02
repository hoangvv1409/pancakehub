from ._base import CRUD
from ..models import ItemSchema


class ItemRepository(CRUD):
    def __init__(self, session):
        self.session = session
        self.model = ItemSchema
