from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app import crud, schemas
from app.api.deps import SessionDep
from app.core.security import create_access_token, set_access_token_cookie

router = APIRouter()


@router.post("/auth/login/")
def login_for_access_token(
    response: Response,
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> schemas.UserPublic:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(user.id)
    set_access_token_cookie(response, access_token)

    return user


@router.post(
    "/auth/register/",
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    response: Response, session: SessionDep, user_in: schemas.UserRegister
) -> schemas.UserPublic:
    """
    Register new user.
    """
    if crud.get_user_by_email(session, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    db_user = crud.create_user(session, user_in)
    access_token = create_access_token(db_user.id)
    set_access_token_cookie(response, access_token)

    return db_user


@router.post("/auth/logout/", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    """
    Remove access token cookie.
    """
    response.delete_cookie("access_token")
