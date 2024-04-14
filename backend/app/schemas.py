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
    profile_pic_url: str | None = None
    dob: date
    gender: GenderEnum
    github_username: str
    linkedin_username: str
    skills: list[str]
    country: str
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


class UserUpdate(BaseModel):
    email: str | None = None
    full_name: str | None = None
    bio: str | None = None
    profile_pic_url: str | None = None
    dob: date | None = None
    gender: GenderEnum | None = None
    github_username: str | None = None
    linkedin_username: str | None = None
    skills: list[str] | None = None
    country: str | None = None
    hobbies: list[str] | None = None
    preferred_buddy_type: BuddyTypeEnum | None = None
    preferred_skills: list[str] | None = None
    preferred_gender: GenderEnum | None = None


class UserMatch(BaseModel):
    id: int
    email: str
    full_name: str
    bio: str | None = None
    profile_pic_url: str | None = None
    dob: date
    gender: GenderEnum
    github_username: str
    linkedin_username: str
    skills: list[str]
    country: str
    hobbies: list[str]

    class Config:
        # Pydantic ORM mode (formerly 'orm_mode')
        from_attributes = True


# Generic message
class Message(BaseModel):
    message: str


# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: int | None = None
