from ._base import CRUD
from ..models import FbPageSchema


class FbPageRepository(CRUD):
    def __init__(self, session):
        self.session = session
        self.model = FbPageSchema
