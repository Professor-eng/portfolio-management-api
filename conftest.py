import asyncio
import os
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool
from limiter import limiter

load_dotenv()

from database import Base, get_db
from main import app

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=NullPool)
TestSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function", autouse=True)
async def reset_limiter():
    limiter.reset()
    yield

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

