from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from model.user import User
from model.medical_staff import MedicalStaff
from schema.medical_staff import UserMedicalStaffCreate, UserMedicalStaffView
from schema.medical_staff import UserMedicalStaffUpdate, UserMedicalStaffViewAll
from utils.password_utils import generate_random_password, hash_password
from config.database import SessionLocal
import random
import string
from typing import List
import hashlib


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create_user_with_medical_staff", response_model=UserMedicalStaffView)
def create_user_with_medical_staff(user_medical_staff: UserMedicalStaffCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya está en uso
    if db.query(User).filter(User.email == user_medical_staff.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
    
    # Verificar si la identification_card ya está en uso
    if db.query(User).filter(User.identification_card == user_medical_staff.identification_card).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Identification card already in use")
    # Generar una contraseña aleatoria
    password = generate_random_password()
    # Encriptar la contraseña
    hashed_password = hash_password(password)
    # Crear el usuario primero
    new_user = User(
        name=user_medical_staff.name,
        last_name=user_medical_staff.last_name,
        identification_card=user_medical_staff.identification_card,
        age=user_medical_staff.age,
        phone=user_medical_staff.phone,
        email=user_medical_staff.email,
        password=hashed_password,
        address=user_medical_staff.address,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Crear el personal médico y asignar al usuario creado
    new_medical_staff = MedicalStaff(
        professional_card=user_medical_staff.professional_card,
        specialty=user_medical_staff.specialty,
        personal_type=user_medical_staff.personal_type,
        user_id=new_user.id,
    )
    db.add(new_medical_staff)
    db.commit()
    db.refresh(new_medical_staff)

    user_medical_staff_view = UserMedicalStaffView(
        id=new_user.id,
        name=new_user.name,
        last_name=new_user.last_name,
        identification_card=new_user.identification_card,
        age=new_user.age,
        phone=new_user.phone,
        email=new_user.email,
        address=new_user.address,
        professional_card=new_medical_staff.professional_card,
        specialty=new_medical_staff.specialty,
        personal_type=new_medical_staff.personal_type,
    )
    return user_medical_staff_view


@router.put("/update_user_with_medical_staff/{medical_staff_id}", response_model=UserMedicalStaffView)
def update_user_with_medical_staff(medical_staff_id: int, user_medical_staff: UserMedicalStaffUpdate, db: Session = Depends(get_db)):
    # Obtener el personal médico existente
    medical_staff = db.query(MedicalStaff).filter(MedicalStaff.id == medical_staff_id).first()

    if not medical_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical staff not found")

    # Obtener el usuario asociado al personal médico
    user = medical_staff.user

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Actualizar los campos del usuario
    for field, value in user_medical_staff.dict(exclude={"password"}).items():
        if field == "identification_card" and value:
            existing_user = db.query(User).filter(User.identification_card == value).first()
            if existing_user and existing_user.id != user.id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Identification card already exists")
        if field == "email" and value:
            existing_user = db.query(User).filter(User.email == value).first()
            if existing_user and existing_user.id != user.id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        setattr(user, field, value)

    # Actualizar los campos del personal médico
    for field, value in user_medical_staff.dict().items():
        if hasattr(medical_staff, field) and field != "id":
            setattr(medical_staff, field, value)

    db.commit()

    user_medical_staff_view = UserMedicalStaffView(
        id=user.id,
        name=user.name,
        last_name=user.last_name,
        identification_card=user.identification_card,
        age=user.age,
        phone=user.phone,
        email=user.email,
        address=user.address,
        professional_card=medical_staff.professional_card,
        specialty=medical_staff.specialty,
        personal_type=medical_staff.personal_type,
    )
    return user_medical_staff_view


@router.delete("/delete_medical_staff/{medical_staff_id}")
def delete_medical_staff(medical_staff_id: int, db: Session = Depends(get_db)):
    # Obtener el personal médico existente
    medical_staff = db.query(MedicalStaff).filter(MedicalStaff.id == medical_staff_id).first()

    if not medical_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical staff not found")

    # Obtener el usuario asociado al personal médico
    user = medical_staff.user

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Eliminar el personal médico
    db.delete(medical_staff)

    # Eliminar el usuario asociado al personal médico
    db.delete(user)

    db.commit()

    return {"message": "Medical staff and associated user deleted successfully"}



@router.get("/get_all_medical_staff", response_model=List[UserMedicalStaffViewAll])
def get_all_medical_staff(db: Session = Depends(get_db)):
    medical_staff = db.query(MedicalStaff).all()

    user_medical_staff_views = []
    for staff in medical_staff:
        user = db.query(User).filter(User.id == staff.user_id).first()
        if user:
            user_medical_staff_view = UserMedicalStaffViewAll(
                id=staff.id,
                name=user.name,
                last_name=user.last_name,
                identification_card=user.identification_card,
                age=user.age,
                phone=user.phone,
                email=user.email,
                address=user.address,
                professional_card=staff.professional_card,
                specialty=staff.specialty,
                personal_type=staff.personal_type,
            )
            user_medical_staff_views.append(user_medical_staff_view)

    return user_medical_staff_views
