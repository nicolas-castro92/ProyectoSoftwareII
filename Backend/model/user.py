from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base, engine

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    last_name = Column(String(255))
    identification_card = Column(String(255), unique=True)
    age = Column(Integer)
    phone = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    address = Column(String(255))

    familiars = relationship("Familiar", back_populates="users")

Base.metadata.create_all(bind=engine)
