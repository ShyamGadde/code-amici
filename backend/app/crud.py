from sqlalchemy import text
from sqlalchemy.orm import Session

from app import schemas
from app.core.security import get_password_hash, verify_password
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


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.query(User).filter(User.email == email).first()


def get_user_matches(session: Session, current_user: User) -> list[schemas.UserMatch]:
    query = text("""
        SELECT id, email, full_name, bio, profile_pic_url, dob, gender, github_username, linkedin_username, skills, country, hobbies
        FROM users u
        WHERE u.id != :current_user_id AND
            (
                (u.preferred_buddy_type = 'Buddy' AND :current_user_preferred_buddy_type = 'Buddy') OR
                (u.preferred_buddy_type = 'Mentor' AND :current_user_preferred_buddy_type = 'Mentee') OR
                (u.preferred_buddy_type = 'Mentee' AND :current_user_preferred_buddy_type = 'Mentor')
            )
            AND u.skills && ARRAY[:current_user_preferred_skills]::varchar[]
            AND ARRAY[:current_user_skills]::varchar[] && u.preferred_skills
            AND (u.gender = :current_user_preferred_gender OR :current_user_preferred_gender = 'Any')
            AND (:current_user_gender = u.preferred_gender OR u.preferred_gender = 'Any')
    """)

    result = session.execute(
        query,
        {
            "current_user_id": current_user.id,
            "current_user_preferred_buddy_type": current_user.preferred_buddy_type,
            "current_user_preferred_skills": current_user.preferred_skills,
            "current_user_skills": current_user.skills,
            "current_user_preferred_gender": current_user.preferred_gender,
            "current_user_gender": current_user.gender,
        },
    )
    return [schemas.UserMatch.model_validate(row) for row in result]


def authenticate(session: Session, email: str, password: str) -> User | None:
    if db_user := get_user_by_email(session, email):
        return db_user if verify_password(password, db_user.hashed_password) else None
    else:
        return None
