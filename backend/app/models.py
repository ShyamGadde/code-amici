"""
SQLAlchemy models for the FastAPI app
"""

from sqlalchemy import (
    ARRAY,
    TIMESTAMP,
    Column,
    Date,
    Enum,
    Index,
    Integer,
    String,
    Text,
    func,
)

from app.database import Base

gender_enum = Enum("Male", "Female", "Any", name="GENDER")
buddy_type_enum = Enum("Buddy", "Mentor", "Mentee", name="BUDDY_TYPE")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    bio = Column(Text)
    profile_pic = Column(String)
    dob = Column(Date, nullable=False)
    gender = Column(gender_enum, index=True, nullable=False)
    github_username = Column(String, nullable=False)
    linkedin_username = Column(String, nullable=False)
    skills = Column(ARRAY(String), nullable=False)
    nationality = Column(String(2), nullable=False)
    hobbies = Column(ARRAY(String), nullable=False)
    preferred_buddy_type = Column(buddy_type_enum, index=True, nullable=False)
    preferred_skills = Column(ARRAY(String), nullable=False)
    preferred_gender = Column(gender_enum, index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
    )


# Create GIN indexes on the 'skills' and 'preferred_skills' columns
Index("ix_users_skills", User.skills, postgresql_using="gin")
Index("ix_users_preferred_skills", User.preferred_skills, postgresql_using="gin")
