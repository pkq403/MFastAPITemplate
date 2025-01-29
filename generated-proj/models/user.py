from sqlalchemy import Column, String, Integer

class User(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
