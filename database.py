from typing import AsyncGenerator
from config import settings
from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker,create_async_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.database_url,echo=False)

AsyncSessionLocal = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

class Base(DeclarativeBase):
    pass