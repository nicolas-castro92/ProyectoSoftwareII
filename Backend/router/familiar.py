from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schema.familiar import FamiliarCreate, FamiliarUpdate, FamiliarView, UserFamiliarCreate, UserFamiliarView, UserFamiliarUpdate
from schema.familiar import UserFamiliarViewAll
from model.familiar import Familiar
from model.user import User
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

@router.get("/familiars/{familiar_id}", response_model=FamiliarView)
def get_familiar(familiar_id: int, db: Session = Depends(get_db)):
    familiar = db.query(Familiar).filter(Familiar.id == familiar_id).first()
    if not familiar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Familiar not found")
    return familiar

@router.post("/familiars", response_model=FamiliarView)
def create_familiar(familiar: FamiliarCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == familiar.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    new_familiar = Familiar(**familiar.dict())
    db.add(new_familiar)
    db.commit()
    db.refresh(new_familiar)
    return new_familiar

@router.get("/familiars", response_model=list[FamiliarView])
def get_all_familiars(db: Session = Depends(get_db)):
    familiars = db.query(Familiar).all()
    return familiars

@router.put("/familiars/{familiar_id}", response_model=FamiliarView)
def update_familiar(familiar_id: int, familiar: FamiliarUpdate, db: Session = Depends(get_db)):
    db.query(Familiar).filter(Familiar.id == familiar_id).update(familiar.dict(exclude_unset=True))
    db.commit()
    updated_familiar = db.query(Familiar).filter(Familiar.id == familiar_id).first()
    if not updated_familiar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Familiar not found")
    return updated_familiar

@router.delete("/familiars/{familiar_id}")
def delete_familiar(familiar_id: int, db: Session = Depends(get_db)):
    deleted_count = db.query(Familiar).filter(Familiar.id == familiar_id).delete()
    db.commit()
    if not deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Familiar not found")
    return {"message": "Familiar deleted"}

@router.post("/create_user_with_familiar", response_model=UserFamiliarView)
def create_user_with_familiar(user_familiar: UserFamiliarCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya está en uso
    if db.query(User).filter(User.email == user_familiar.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
    
    # Verificar si la identification_card ya está en uso
    if db.query(User).filter(User.identification_card == user_familiar.identification_card).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Identification card already in use")

    # Generar una contraseña aleatoria
    password = generate_random_password()

    # Crear el usuario primero
    new_user = User(
        name=user_familiar.name,
        last_name=user_familiar.last_name,
        identification_card=user_familiar.identification_card,
        age=user_familiar.age,
        phone=user_familiar.phone,
        email=user_familiar.email,
        password=password,
        address=user_familiar.address,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Crear el familiar y asignar al usuario creado
    new_familiar = Familiar(
        alternate_phone=user_familiar.alternate_phone,
        user_id=new_user.id,
    )
    db.add(new_familiar)
    db.commit()
    db.refresh(new_familiar)

    user_familiar_view = UserFamiliarView(
        id=new_user.id,
        name=new_user.name,
        last_name=new_user.last_name,
        identification_card=new_user.identification_card,
        age=new_user.age,
        phone=new_user.phone,
        email=new_user.email,
        password=password,
        address=new_user.address,
        familiar_id=new_familiar.id,
        alternate_phone=new_familiar.alternate_phone,
    )
    return user_familiar_view

def generate_random_password(length=5):
    digits = string.digits
    return ''.join(random.choice(digits) for _ in range(length))

@router.put("/update_user_with_familiar/{user_id}", response_model=UserFamiliarView)
def update_user_with_familiar(user_id: int, user_familiar: UserFamiliarUpdate, db: Session = Depends(get_db)):
    # Obtener el usuario y el familiar existentes
    user = db.query(User).filter(User.id == user_id).first()
    familiar = db.query(Familiar).filter(Familiar.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not familiar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Familiar not found")

    # Actualizar los campos del usuario
    for field, value in user_familiar.dict(exclude={"password"}).items():
        if field == "identification_card" and value:
            existing_user = db.query(User).filter(User.identification_card == value).first()
            if existing_user and existing_user.id != user_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Identification card already exists")
        if field == "email" and value:
            existing_user = db.query(User).filter(User.email == value).first()
            if existing_user and existing_user.id != user_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        setattr(user, field, value)

    # Actualizar los campos del familiar
    for field, value in user_familiar.dict().items():
        if hasattr(familiar, field) and field != "user_id":
            setattr(familiar, field, value)

    db.commit()

    user_familiar_view = UserFamiliarView(
        id=user.id,
        name=user.name,
        last_name=user.last_name,
        identification_card=user.identification_card,
        age=user.age,
        phone=user.phone,
        email=user.email,
        password=user.password,
        address=user.address,
        familiar_id=familiar.id,
        alternate_phone=familiar.alternate_phone,
    )
    return user_familiar_view


@router.delete("/delete_familiar/{familiar_id}")
def delete_familiar(familiar_id: int, db: Session = Depends(get_db)):
    # Obtener el familiar existente
    familiar = db.query(Familiar).filter(Familiar.id == familiar_id).first()

    if not familiar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Familiar not found")

    # Obtener el usuario asociado al familiar
    user = db.query(User).filter(User.id == familiar.user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Eliminar el familiar
    db.delete(familiar)

    # Eliminar el usuario asociado al familiar
    db.delete(user)

    db.commit()

    return {"message": "Familiar and associated user deleted successfully"}

@router.get("/get_all_familiars", response_model=List[UserFamiliarViewAll])
def get_all_familiars(db: Session = Depends(get_db)):
    familiars = db.query(Familiar).all()

    user_familiar_views = []
    for familiar in familiars:
        user = db.query(User).filter(User.id == familiar.user_id).first()
        if user:
            user_familiar_view = UserFamiliarViewAll(
                name=user.name,
                last_name=user.last_name,
                identification_card=user.identification_card,
                age=user.age,
                phone=user.phone,
                email=user.email,
                address=user.address,
                alternate_phone=familiar.alternate_phone,
            )
            user_familiar_views.append(user_familiar_view)

    return user_familiar_views
