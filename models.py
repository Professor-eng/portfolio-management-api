from sqlalchemy import String, Integer, DateTime, Float, Numeric, func, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum
from database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    portfolio_items: Mapped[list["PortfolioItem"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    watchlist_items: Mapped[list["WatchlistItem"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class PortfolioItem(Base):
    __tablename__ = "portfolio_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    stock_symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    average_price: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="portfolio_items")


class AlertCondition(str, enum.Enum):
    above = "above"
    below = "below"

class Alert(Base):
    __tablename__ = "alerts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    condition: Mapped[AlertCondition] = mapped_column(Enum(AlertCondition), nullable=False)
    target_price: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="alerts")


class WatchlistItem(Base):
    __tablename__ = "watchlist_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    added_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="watchlist_items")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token: Mapped[str] = mapped_column(String(512), nullable=False, unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")