from ._base import CRUD
from ..models import PartnerSchema


class PartnerRepository(CRUD):
    def __init__(self, session):
        self.session = session
        self.model = PartnerSchema
