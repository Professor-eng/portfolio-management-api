from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import User, WatchlistItem
from schemas import WatchlistItemCreate, WatchlistItemOut
from security import get_current_user

router = APIRouter(prefix="/watchlist", tags=["watchlist"])

@router.get("/", response_model=list[WatchlistItemOut])
async def get_watchlist(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]):
    result = await db.execute(select(WatchlistItem).where(WatchlistItem.user_id == current_user.id))
    return result.scalars().all()

@router.post("/", response_model=WatchlistItemOut)
async def add_watchlist_item(item: WatchlistItemCreate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]):
    new_item = WatchlistItem(user_id=current_user.id, symbol=item.symbol)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.delete("/{item_id}")
async def delete_watchlist_item(item_id: int, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]):
    result = await db.execute(select(WatchlistItem).where(WatchlistItem.id == item_id, WatchlistItem.user_id == current_user.id))
    existing = result.scalar_one_or_none()
    if not existing:
        raise HTTPException(status_code=404, detail="Watchlist item not found")
    await db.delete(existing)
    await db.commit()
    return {"message": "Deleted"}