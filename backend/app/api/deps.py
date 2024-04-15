from typing import Annotated, Generator

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm.session import Session

from app import models, schemas
from app.core import security
from app.core.config import settings
from app.core.db import SessionLocal
from app.core.security import OAuth2PasswordBearerWithCookie

reusable_oauth2 = OAuth2PasswordBearerWithCookie(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/"
)


# For an independent database session per request
def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as db:
        yield db


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from e
    if user := session.query(models.User).get(token_data.sub):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


CurrentUser = Annotated[models.User, Depends(get_current_user)]
