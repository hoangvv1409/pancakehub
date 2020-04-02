from ._base import CRUD
from ..models import ShopSchema


class ShopRepository(CRUD):
    def __init__(self, session):
        self.session = session
        self.model = ShopSchema
