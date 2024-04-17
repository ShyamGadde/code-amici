"""
SQLAlchemy models for the FastAPI app
"""

from sqlalchemy import (
    ARRAY,
    TIMESTAMP,
    Column,
    Date,
    Enum,
    Integer,
    String,
    Text,
    func,
)

from app.core.db import Base

gender_enum = Enum("Male", "Female", name="GENDER")
goal_enum = Enum("Build Projects", "Prepare for Coding Interviews", "Both", name="GOAL")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    bio = Column(Text)
    profile_image = Column(String)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(gender_enum, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    github_profile = Column(String, nullable=False)
    linkedin_profile = Column(String, nullable=False)
    skill_proficiencies = Column(ARRAY(String), nullable=False)
    highest_education = Column(Text, nullable=False)
    experience_years = Column(Integer, nullable=False)
    hobbies = Column(ARRAY(String), nullable=False)
    languages = Column(ARRAY(String), nullable=False)
    goal = Column(goal_enum, nullable=False)
    commitment_hours = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
    )
