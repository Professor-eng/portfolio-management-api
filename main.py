from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from portfolio import router as portfolio_router
from alerts import router as alerts_router
from watchlist import router as watchlist_router
from database import engine, Base
from contextlib import asynccontextmanager
from limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(portfolio_router)
app.include_router(alerts_router)
app.include_router(watchlist_router)


app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
