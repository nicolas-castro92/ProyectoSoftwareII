from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base, engine

class PersonalInCharge(Base):
    __tablename__ = "personal_in_charge"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    medical_staff_id = Column(Integer, ForeignKey("medical_staff.id"))

    medical_staff = relationship("MedicalStaff", back_populates="assigned_patients")
    patient = relationship("Patient", back_populates="assigned_medical_staff")


Base.metadata.create_all(bind=engine)