from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from schema.user import UserCreate, UserUpdate, UserView
from model.user import User
from config.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users", response_model=list[UserView])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.post("/users", response_model=UserView)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe un usuario con el mismo número de identificación
    existing_user = db.query(User).filter(User.identification_card == user.identification_card).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this identification card already exists")

    # Verificar si ya existe un usuario con el mismo correo electrónico
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/{user_id}", response_model=UserView)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user

@router.put("/users/{user_id}", response_model=UserView)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db.query(User).filter(User.id == user_id).update(user.dict(exclude_unset=True))
    db.commit()
    updated_user = db.query(User).filter(User.id == user_id).first()
    return updated_user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
    return {"message": "User deleted"}

@router.get("/users/identification_card/{card_number}", response_model=UserView)
def get_user_by_identification_card(card_number: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.identification_card == card_number).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

