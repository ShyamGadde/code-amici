from sqlalchemy import text
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


def get_user_matches(session: Session, current_user: User) -> list[schemas.UserMatch]:
    # TODO: Use current user parameters directly in WHERE clause conditions instead of a subquery
    query = text("""
        SELECT id, email, full_name, bio, profile_pic_url, dob, gender, github_username, linkedin_username, skills, country, hobbies
        FROM users u1
        WHERE EXISTS (
            SELECT 1
            FROM users u2
            WHERE u2.id = :current_user_id AND u1.id != u2.id AND
                (
                    (u1.preferred_buddy_type = 'Buddy' AND u2.preferred_buddy_type = 'Buddy') OR
                    (u1.preferred_buddy_type = 'Mentor' AND u2.preferred_buddy_type = 'Mentee') OR
                    (u1.preferred_buddy_type = 'Mentee' AND u2.preferred_buddy_type = 'Mentor')
                )
                AND u1.skills && u2.preferred_skills
                AND u2.skills && u1.preferred_skills
                AND (u1.gender = u2.preferred_gender OR u2.preferred_gender = 'Any')
                AND (u2.gender = u1.preferred_gender OR u1.preferred_gender = 'Any')
        )
        """)

    result = session.execute(query, {"current_user_id": current_user.id})
    matches = [schemas.UserMatch.model_validate(row) for row in result]
    return matches


def update_user(session: Session, user: User, user_in: schemas.UserUpdate) -> User:
    update_data = user_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    session.commit()
    session.refresh(user)
    return user
