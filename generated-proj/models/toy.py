from sqlalchemy import Column, String, Integer

class Toy(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
