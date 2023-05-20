from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schema.user import UserCreate, UserUpdate, UserView
from model.user import User
from config.database import get_db

router = APIRouter()

@router.get("/users", response_model=list[UserView])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.post("/users", response_model=UserView)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
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
