from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import User, PortfolioItem
from schemas import PortfolioItemCreate, PortfolioItemOut
from security import get_current_user

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

@router.get("/", response_model=list[PortfolioItemOut])
async def get_portfolio(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]):
    result = await db.execute(select(PortfolioItem).where(PortfolioItem.user_id == current_user.id))
    return result.scalars().all()

@router.post("/", response_model=PortfolioItemOut)
async def add_portfolio_item(item: PortfolioItemCreate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]):
    new_item = PortfolioItem(user_id=current_user.id, stock_symbol=item.stockSymbol, quantity=item.quantity, average_price=item.averagePrice)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.put("/{item_id}", response_model=PortfolioItemOut)
async def update_portfolio_item(item_id: int, item: PortfolioItemCreate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]):
    result = await db.execute(select(PortfolioItem).where(PortfolioItem.id == item_id, PortfolioItem.user_id == current_user.id))
    existing = result.scalar_one_or_none()
    if not existing:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    existing.stock_symbol = item.stockSymbol
    existing.quantity = item.quantity
    existing.average_price = item.averagePrice
    await db.commit()
    await db.refresh(existing)
    return existing

@router.delete("/{item_id}")
async def delete_portfolio_item(item_id: int, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]):
    result = await db.execute(select(PortfolioItem).where(PortfolioItem.id == item_id, PortfolioItem.user_id == current_user.id))
    existing = result.scalar_one_or_none()
    if not existing:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    await db.delete(existing)
    await db.commit()
    return {"message": "Deleted"}