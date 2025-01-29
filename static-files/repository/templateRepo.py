from .abstractRepo import AbstractRepository
from sqlalchemy.orm import Session
from ..models import Template

class TemplateRepository(AbstractRepository):
    def __init__(self):
        self.entity = Template