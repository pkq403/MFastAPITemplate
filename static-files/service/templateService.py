from sqlalchemy.orm import Session
from ..repositories import TemplateRepository

class TemplateService:
    '''
    Logs table interface
    '''
    def __init__(self):
        self.repo = TemplateRepository()