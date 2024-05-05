import pickle
from typing import Any

import redis.asyncio as redis
from fastapi import APIRouter, HTTPException, Request, Response, status

from app import crud, schemas
from app.api.deps import CurrentUser, SessionDep
from app.recommendations import get_buddy_recommendations

router = APIRouter()


@router.get("/me/", response_model=schemas.UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user


@router.get("/me/recommendations/", response_model=list[schemas.UserMatch])
async def get_user_recommendations(
    request: Request, session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Retrieve recommendations for current user.
    """
    key = f"recommendations:{current_user.id}"
    redis_client = redis.Redis.from_pool(request.app.state.redis_pool)

    recommendations = await redis_client.get(key)

    if not recommendations:
        recommendations = get_buddy_recommendations(current_user, session)
        recommendations_dict = [user.to_dict() for user in recommendations]
        recommendations_serialized = pickle.dumps(recommendations_dict)

        await redis_client.set(key, recommendations_serialized, ex=3600)
    else:  # Cache hit
        print("INFO:\tCache hit - TTL:", await redis_client.ttl(key), "seconds")
        recommendations = pickle.loads(recommendations)

    await redis_client.close()

    return recommendations


@router.patch("/me/", response_model=schemas.UserPublic)
async def update_user_me(
    request: Request,
    session: SessionDep,
    current_user: CurrentUser,
    user_in: schemas.UserUpdate,
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

    # Invalidate recommendations cache
    key = f"recommendations:{current_user.id}"
    redis_client = redis.Redis.from_pool(request.app.state.redis_pool)

    await redis_client.delete(key)

    await redis_client.close()

    return current_user


@router.delete("/me/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_me(response: Response, session: SessionDep, current_user: CurrentUser):
    """
    Delete own user.
    """
    session.delete(current_user)
    session.commit()
    response.delete_cookie("access_token")
