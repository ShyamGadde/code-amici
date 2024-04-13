from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy.orm.session import Session

from app.database import SessionLocal


# For an independent database session per request
def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as db:
        yield db


SessionDep = Annotated[Session, Depends(get_db)]
