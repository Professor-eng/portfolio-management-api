from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import User, Alert
from schemas import AlertCreate, AlertOut
from security import get_current_user

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/", response_model=list[AlertOut])
async def get_alerts(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]):
    result = await db.execute(select(Alert).where(Alert.user_id == current_user.id))
    return result.scalars().all()

@router.post("/", response_model=AlertOut)
async def create_alert(alert: AlertCreate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]):
    new_alert = Alert(user_id=current_user.id, symbol=alert.symbol, condition=alert.condition, target_price=alert.targetPrice)
    db.add(new_alert)
    await db.commit()
    await db.refresh(new_alert)
    return new_alert

@router.delete("/{alert_id}")
async def delete_alert(alert_id: int, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]):
    result = await db.execute(select(Alert).where(Alert.id == alert_id, Alert.user_id == current_user.id))
    existing = result.scalar_one_or_none()
    if not existing:
        raise HTTPException(status_code=404, detail="Alert not found")
    await db.delete(existing)
    await db.commit()
    return {"message": "Deleted"}