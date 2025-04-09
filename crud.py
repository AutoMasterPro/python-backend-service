from sqlalchemy.orm import Session
import models
import schemas
import auth


def create_user(db: Session, user: schemas.UserCreate):
    hashed_pwd = auth.hash_password(user.password)
    db_user = models.User(name=user.name, email=user.email, phone=user.phone, hashed_password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user and auth.verify_password(password, user.hashed_password):
        return user
    return None

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
