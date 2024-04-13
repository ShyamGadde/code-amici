from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserRegister


def get_user(session: Session, user_id: int):
    return session.query(User).filter(User.id == user_id).first()


def create_user(session: Session, user: UserRegister):
    # TODO: Hash the password before storing it in the database
    hashed_password = user.password
    db_user = User(**user.model_dump(), hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
