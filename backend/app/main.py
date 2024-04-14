from datetime import timedelta
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import crud, models, schemas
from app.api.deps import CurrentUser, SessionDep
from app.core import security
from app.core.config import settings
from app.database import engine
from app.matches import rank_matches

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/api/v1/login/access-token/")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> schemas.Token:
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
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return schemas.Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@app.post(
    "/users/signup/",
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
    return schemas.Message(message="New user registered successfully")


@app.get("/users/me/", response_model=schemas.UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user


@app.get("/users/me/matches/", response_model=list[schemas.UserMatch])
def get_user_matches(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Retrieve matches for current user.
    """
    matches = crud.get_user_matches(session, current_user)
    matches = rank_matches(current_user, matches)
    return matches


@app.patch("/users/me/", response_model=schemas.UserPublic)
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


@app.delete("/users/me/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_me(session: SessionDep, current_user: CurrentUser):
    """
    Delete own user.
    """
    session.delete(current_user)
    session.commit()
