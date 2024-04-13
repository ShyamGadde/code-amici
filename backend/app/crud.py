from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate):
    # TODO: Hash the password before storing it in the database
    hashed_password = user.password
    db_user = User(**user.model_dump(), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
