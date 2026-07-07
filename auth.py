from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from datetime import datetime, timedelta, timezone
from models import User, RefreshToken
from database import get_db
from schemas import UserCreate, UserLogin, TokenPair, RefreshRequest
from security import hash_password, verify_password, create_token, create_refresh_token
from limiter import limiter
from fastapi import Request  

router = APIRouter()

@router.post("/auth/register")
@limiter.limit("5/minute")
async def register(request: Request,user_info: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(User).where(
        or_(User.username == user_info.username, User.email == user_info.email)
    ))
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{user_info.username} already exists")

    hash_pass = hash_password(user_info.password)
    new_entry = User(username=user_info.username, email=user_info.email, hashed_password=hash_pass)
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)

    return {"message": "New user created successfully!"}


@router.post("/auth/login", response_model=TokenPair)
@limiter.limit("5/minute")
async def login(request: Request, user_info: UserLogin, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(User).where(User.username == user_info.username))
    existing = result.scalar_one_or_none()

    if not existing:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    if not verify_password(user_info.password, existing.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = create_token(existing.id)
    refresh_token_str = create_refresh_token()

    db.add(RefreshToken(
        user_id=existing.id,
        token=refresh_token_str,
        expires_at=datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=7),
    ))
    await db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token_str, "token_type": "bearer"}


@router.post("/auth/refresh", response_model=TokenPair)
async def refresh(body: RefreshRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(RefreshToken).where(RefreshToken.token == body.refresh_token))
    stored = result.scalar_one_or_none()

    if not stored or stored.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    new_access = create_token(stored.user_id)
    return {"access_token": new_access, "refresh_token": body.refresh_token, "token_type": "bearer"}


@router.post("/auth/logout")
async def logout(body: RefreshRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(RefreshToken).where(RefreshToken.token == body.refresh_token))
    stored = result.scalar_one_or_none()
    if stored:
        await db.delete(stored)
        await db.commit()
    return {"message": "Logged out"}