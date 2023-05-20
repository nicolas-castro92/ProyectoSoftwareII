from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base, engine

class MedicalStaff(Base):
    __tablename__ = "medical_staff"

    id = Column(Integer, primary_key=True, index=True)
    professional_card = Column(String(255))
    specialty = Column(String(255))
    personal_type = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="medical_staff")

Base.metadata.create_all(bind=engine)
