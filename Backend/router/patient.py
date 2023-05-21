from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from model.user import User
from model.patient import Patient
from schema.patient import UserPatientCreate, UserPatientView
from schema.patient import UserPatientUpdate, UserPatientViewAll
from config.database import SessionLocal
import random
import string
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    
@router.post("/create_user_with_patient", response_model=UserPatientView)
def create_user_with_patient(user_patient: UserPatientCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya está en uso
    if db.query(User).filter(User.email == user_patient.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
    
    # Verificar si la identification_card ya está en uso
    if db.query(User).filter(User.identification_card == user_patient.identification_card).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Identification card already in use")

    # Crear el usuario primero
    new_user = User(
        name=user_patient.name,
        last_name=user_patient.last_name,
        identification_card=user_patient.identification_card,
        age=user_patient.age,
        phone=user_patient.phone,
        email=user_patient.email,
        address=user_patient.address,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Crear el paciente y asignar al usuario creado
    new_patient = Patient(
        familiar_id=user_patient.familiar_id,
        user_id=new_user.id,
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    user_patient_view = UserPatientView(
        id=new_user.id,
        name=new_user.name,
        last_name=new_user.last_name,
        identification_card=new_user.identification_card,
        age=new_user.age,
        phone=new_user.phone,
        email=new_user.email,
        address=new_user.address,
    )
    return user_patient_view
