from abc import ABC
from sqlalchemy.orm import Session
from sqlalchemy import and_, text
from typing import List
from datetime import datetime
from ..models import DeletedRecord
from .utils import object_as_dict

'''
IMPORTANT! -> DML operations (INSERT, UPDATE) aren't commited in this repo
(This is useful if u want to use multiple repositories methods in a repostory to commit all operations at the same time)
(If u are sure u wont do multiple repositories operations u could commit in this abstract repository)
'''


class AbstractRepository(ABC):

    def __init__(self):
        self.entity: object

    def add(self, entity: object, db: Session) -> object:
        db.add(entity)
        return entity

    def update(self, entity_id: int, updated_data: dict, db: Session) -> object | None:
        row_to_update = db.query(self.entity).filter(
            self.entity.id == entity_id).first()
        if row_to_update:
            for key, value in updated_data.items():
                if value:
                    setattr(row_to_update, key, value)
            return row_to_update
        return None

    def delete(self, row_id: int, db: Session) -> object | None:
        row_to_delete = db.query(self.entity).filter(
            self.entity.id == row_id).one()
        if row_to_delete is None:
            return None
        row_dict = object_as_dict(row_to_delete)
        db.delete(row_to_delete)
        deleted_record = DeletedRecord(
            original_table=self.entity.__tablename__, 
            original_id=row_id, data=row_dict)
        db.add(deleted_record)
        return row_dict

    def check(self, db: Session, **kwargs):
        filters = set()
        for k, v in kwargs.items():
            filters.add(getattr(self.entity, k) == v)
        return db.query(self.entity).filter(and_(*filters)).first() is not None

    def get_all(self, db: Session) -> List[object]:
        return db.query(self.entity).all()

    def get_by_id(self, id: int, db: Session) -> object:
        return db.query(self.entity).filter(self.entity.id == id).one_or_none()

    def find_by_id(self, id: int, db: Session) -> object:
        return db.query(self.entity).filter(self.entity.id == id).first()

    def get_by_created_datetime_range(self, from_datetime: datetime, to_datetime: datetime, db: Session) -> List[object]:
        return db.query(self.entity).filter(self.entity.created_datetime >= from_datetime and self.entity.created_datetime <= to_datetime)
