from typing import Any

from app import crud, schemas
from app.api.deps import CurrentUser, SessionDep
from app.matches import rank_matches
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.post(
    "/signup/",
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    session: SessionDep, user_in: schemas.UserRegister
) -> schemas.Message:
    """
    Create new user.
    """
    if crud.get_user_by_email(session, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    crud.create_user(session, user_in)
    # TODO: Create a JWT token and return it
    return schemas.Message(message="New user registered successfully")


@router.get("/me/", response_model=schemas.UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user


@router.get("/me/matches/", response_model=list[schemas.UserMatch])
def get_user_matches(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Retrieve matches for current user.
    """
    matches = crud.get_user_matches(session, current_user)
    matches = rank_matches(current_user, matches)
    return matches


@router.patch("/me/", response_model=schemas.UserPublic)
def update_user_me(
    session: SessionDep, current_user: CurrentUser, user_in: schemas.UserUpdate
) -> Any:
    """
    Update own user.
    """
    if user_in.email:
        existing_user = crud.get_user_by_email(session, user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )
    user_data = user_in.model_dump(exclude_unset=True)
    for field, value in user_data.items():
        setattr(current_user, field, value)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.delete("/me/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_me(session: SessionDep, current_user: CurrentUser):
    """
    Delete own user.
    """
    session.delete(current_user)
    session.commit()
