from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schema.familiar import FamiliarCreate, FamiliarUpdate, FamiliarView
from model.familiar import Familiar
from model.user import User
from config.database import SessionLocal

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
