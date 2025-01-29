from sqlalchemy import Column, Integer

class UserToy(Base):
    user_id = Column(Integer, nullable=False, primary_key=True, ForeignKey(user.id))
    toy_id = Column(Integer, nullable=False, primary_key=True, ForeignKey(toy.id))

    __table_args__ = Column(PrimaryKeyConstraint(user.id,toy.id))
