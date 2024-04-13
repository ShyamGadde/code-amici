from sqlalchemy.orm import Session

from app import schemas
from app.core.security import get_password_hash
from app.models import User


def create_user(session: Session, user: schemas.UserRegister) -> User:
    user_create = schemas.User(
        **user.model_dump(), hashed_password=get_password_hash(user.password)
    )
    db_user = User(**user_create.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user(session: Session, user_id: int) -> User | None:
    return session.query(User).get(user_id)


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.query(User).filter(User.email == email).first()
