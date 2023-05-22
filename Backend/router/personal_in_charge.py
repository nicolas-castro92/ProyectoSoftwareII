from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import APIRouter
from sqlalchemy.orm import Session
from model.patient import  Patient
from model.medical_staff import  MedicalStaff
from model.personal_in_charge import  PersonalInCharge
from config.database import SessionLocal

personal_in_charge = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
             
@personal_in_charge.post("/api/assign-medical-staff")
def assign_medical_staff(medical_staff_id: int,patient_id: int, db: Session = Depends(get_db)):
    
    # Verificar si el personal médico y el paciente existen en la base de datos
    medical_staff = db.query(MedicalStaff).filter(MedicalStaff.id == medical_staff_id).first()
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not medical_staff and not patient:
        raise HTTPException(status_code=404, detail="Personal y Paciente no encontrado")
    if not medical_staff:
        raise HTTPException(status_code=404, detail="Personal médico no encontrado")
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
        
    
    # Crear la asignación en la tabla intermedia AssignedStaff
    assigned_staff = PersonalInCharge(medical_staff_id=medical_staff_id, patient_id=patient_id)
    db.add(assigned_staff)
    db.commit()

    return {"message": "Personal médico asignado exitosamente al paciente"}