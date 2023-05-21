from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base, engine

class Familiar(Base):
    __tablename__ = "familiars"

    id = Column(Integer, primary_key=True, index=True)
    alternate_phone = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="familiars")
    patients = relationship("Patient", back_populates="familiar")

Base.metadata.create_all(bind=engine)
