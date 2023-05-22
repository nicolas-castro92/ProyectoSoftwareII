from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base, engine

class PersonalInCharge(Base):
    __tablename__ = "personal_in_charge"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("patients.id"))
    personal_id = Column(Integer, ForeignKey("medical_staff.id"))

    paciente = relationship("Patient", back_populates="personal_a_cargo")
    personal = relationship("MedicalStaff", back_populates="pacientes_a_cargo")

Base.metadata.create_all(bind=engine)