from typing import Any

from fastapi import FastAPI, HTTPException

from app import crud, models, schemas
from app.api.deps import SessionDep
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/users/me/", response_model=schemas.UserPublic)
def read_users_me(user_id: int, session: SessionDep):
    db_user = crud.get_user(session, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/signup/", response_model=schemas.UserPublic)
def register_user(session: SessionDep, user_in: schemas.UserRegister) -> Any:
    if crud.get_user_by_email(session, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(session, user_in)
    return user
