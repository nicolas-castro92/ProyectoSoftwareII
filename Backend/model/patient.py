from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base, engine


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    familiar_id = Column(Integer, ForeignKey("familiars.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    familiar = relationship("Familiar", back_populates="patients")
    user = relationship("User", back_populates="patients")
    
Base.metadata.create_all(bind=engine)