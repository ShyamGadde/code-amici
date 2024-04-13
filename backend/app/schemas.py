"""
Pydantic models for the FastAPI app
"""

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel


class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
    any = "Any"


class BuddyTypeEnum(str, Enum):
    buddy = "Buddy"
    mentor = "Mentor"
    mentee = "Mentee"


class UserBase(BaseModel):
    email: str
    full_name: str
    bio: str | None = None
    profile_pic: str | None = None
    dob: date
    gender: GenderEnum
    github_username: str
    linkedin_username: str
    skills: list[str]
    nationality: str
    hobbies: list[str]
    preferred_buddy_type: BuddyTypeEnum
    preferred_skills: list[str]
    preferred_gender: GenderEnum


class UserRegister(UserBase):
    password: str


class User(UserBase):
    id: int | None = None
    hashed_password: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        # Pydantic ORM mode (formerly 'orm_mode')
        from_attributes = True


class UserPublic(UserBase):
    id: int

    class Config:
        # Pydantic ORM mode (formerly 'orm_mode')
        from_attributes = True
