from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from model.user import User
from model.patient import Patient
from model.familiar import Familiar
from schema.patient import UserPatientCreate, UserPatientView
from schema.patient import UserPatientUpdate, UserPatientViewAll, UserPatientFamiliarView
from utils.password_utils import generate_random_password, hash_password
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

    
@router.post("/create_user_with_patient_familiar", response_model=UserPatientView)
def create_user_with_patient(user_patient: UserPatientCreate, db: Session = Depends(get_db)):
    try:
        # Verificar si el email ya está en uso
        if db.query(User).filter(User.email == user_patient.email).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")

        # Verificar si la identification_card ya está en uso
        if db.query(User).filter(User.identification_card == user_patient.identification_card).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Identification card already in use")

        # Verificar si se proporciona familiar_id
        if user_patient.familiar_id is not None:
            # Validar el familiar_id
            familiar = db.query(Familiar).filter(Familiar.id == user_patient.familiar_id).first()
            if not familiar:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid familiar_id")

            # Crear el paciente y asignar al usuario y familiar
            new_patient = Patient(
                familiar_id=user_patient.familiar_id,
            )
        else:
            # Crear el paciente y asignar solo al usuario
            new_patient = Patient()

        # Generar una contraseña aleatoria
        password = generate_random_password()
        # Crear el usuario primero
        hashed_password = hash_password(password)
        new_user = User(
            name=user_patient.name,
            last_name=user_patient.last_name,
            identification_card=user_patient.identification_card,
            age=user_patient.age,
            phone=user_patient.phone,
            email=user_patient.email,
            address=user_patient.address,
            password=hashed_password,
            patients=[new_patient]  # Asignar el paciente al usuario
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

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

    except Exception as e:
        db.rollback()  # Revertir la transacción en caso de excepción
        raise e


def generate_random_password(length=5):
    digits = string.digits
    return ''.join(random.choice(digits) for _ in range(length))


@router.put("/update_user_with_patient/{patient_id}", response_model=UserPatientView)
def update_user_with_patient(patient_id: int, user_patient: UserPatientUpdate, db: Session = Depends(get_db)):
    # Obtener el paciente existente
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    # Obtener el usuario asociado al paciente
    user = patient.user

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Actualizar los campos del paciente
    if hasattr(user_patient, "familiar_id") and user_patient.familiar_id is not None:
        # Verificar si se proporciona familiar_id
        familiar = db.query(Familiar).filter(Familiar.id == user_patient.familiar_id).first()
        if not familiar:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid familiar_id")

        patient.familiar_id = user_patient.familiar_id

    db.commit()

    user_patient_view = UserPatientView(
        id=user.id,
        name=user.name,
        last_name=user.last_name,
        identification_card=user.identification_card,
        age=user.age,
        phone=user.phone,
        email=user.email,
        address=user.address,
        familiar_id=patient.familiar_id
    )
    return user_patient_view

@router.delete("/delete_patient/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    # Obtener el paciente existente
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    # Obtener el usuario asociado al paciente
    user = patient.user

    if user:
        # Eliminar el paciente y el usuario asociado
        db.delete(patient)
        db.delete(user)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.commit()


@router.get("/all_user_patient_familiar", response_model=List[UserPatientFamiliarView])
def get_all_user_patient_familiar(db: Session = Depends(get_db)):
    patients = (
        db.query(Patient)
        .join(User)
        .options(joinedload(Patient.familiar).joinedload(Familiar.user))
        .all()
    )
    user_patient_familiar_list = []

    for patient in patients:
        user = patient.user
        familiar = patient.familiar

        user_patient_familiar = UserPatientFamiliarView(
            user_id=user.id,
            name=user.name,
            last_name=user.last_name,
            identification_card=user.identification_card,
            age=user.age,
            phone=user.phone,
            email=user.email,
            address=user.address,
            patient_id=patient.id,
            familiar_id=familiar.id if familiar else None,
            familiar_name=familiar.user.name if familiar else None,
            familiar_last_name=familiar.user.last_name if familiar else None,
            familiar_identification_card=familiar.user.identification_card if familiar else None,
            familiar_age=familiar.user.age if familiar else None,
            familiar_phone=familiar.user.phone if familiar else None,
            familiar_email=familiar.user.email if familiar else None,
            familiar_address=familiar.user.address if familiar else None,
            familiar_alternate_phone=familiar.alternate_phone if familiar else None,
        )

        user_patient_familiar_list.append(user_patient_familiar)

    return user_patient_familiar_list
