from fastapi import FastAPI, HTTPException

from app import crud, models
from app.api.deps import SessionDep
from app.database import engine
from app.schemas import User

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/users/me/", response_model=User)
def read_users_me(user_id: int, session: SessionDep):
    db_user = crud.get_user(session, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
