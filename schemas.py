from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime



class UserCreate(BaseModel):
    username: str = Field(...,min_length=3,max_length=50,)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    username: str = Field(...,min_length=3,max_length=50,)
    password: str = Field(..., min_length=8)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(...,min_length=3,max_length=50,)
    id: int
    email: EmailStr



class PortfolioItemCreate(BaseModel):
    stockSymbol: str = Field(..., min_length=1, max_length=20)
    quantity: int = Field(..., gt=0)
    averagePrice: float = Field(..., gt=0)

class PortfolioItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    stockSymbol: str = Field(validation_alias="stock_symbol")
    quantity: int
    averagePrice: float = Field(validation_alias="average_price")

class AlertCreate(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20)
    condition: str = Field(..., pattern="^(above|below)$")
    targetPrice: float = Field(..., gt=0)

class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    symbol: str
    condition: str
    targetPrice: float = Field(validation_alias="target_price")

class WatchlistItemCreate(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20)

class WatchlistItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    symbol: str
    added_at: datetime

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str