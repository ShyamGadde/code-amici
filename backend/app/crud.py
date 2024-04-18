from sqlalchemy.orm import Session

from app import schemas
from app.core.security import get_password_hash, verify_password
from app.models import User


def create_user(session: Session, user: schemas.UserRegister) -> User:
    user_create = schemas.User(**user.model_dump())
    user_create.password = get_password_hash(user.password)
    db_user = User(**user_create.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.query(User).filter(User.email == email).first()


def authenticate(session: Session, email: str, password: str) -> User | None:
    if db_user := get_user_by_email(session, email):
        return db_user if verify_password(password, db_user.password) else None
    else:
        return None
