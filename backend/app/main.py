from typing import Any

from fastapi import FastAPI, HTTPException, status

from app import crud, models, schemas
from app.api.deps import SessionDep
from app.database import engine
from app.matches import rank_matches

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post(
    "/users/signup/",
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    session: SessionDep, user_in: schemas.UserRegister
) -> schemas.Message:
    if crud.get_user_by_email(session, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    crud.create_user(session, user_in)
    return schemas.Message(message="New user registered successfully")


@app.get("/users/me/", response_model=schemas.UserPublic)
def read_user_me(user_id: int, session: SessionDep) -> Any:
    db_user = crud.get_user(session, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@app.get("/users/me/matches/", response_model=list[schemas.UserMatch])
def get_user_matches(user_id: int, session: SessionDep) -> Any:
    db_user = crud.get_user(session, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    matches = crud.get_user_matches(session, db_user)
    matches = rank_matches(db_user, matches)
    return matches


@app.patch("/users/me/", response_model=schemas.UserPublic)
def update_user_me(
    user_id: int, session: SessionDep, user_in: schemas.UserUpdate
) -> Any:
    db_user = crud.get_user(session, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db_user = crud.update_user(session, db_user, user_in)
    return db_user


@app.delete("/users/me/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_me(user_id: int, session: SessionDep):
    db_user = crud.get_user(session, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    session.delete(db_user)
    session.commit()
