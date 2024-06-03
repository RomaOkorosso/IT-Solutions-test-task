import os

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from app.src import auth_router, good_router, good_service
from app.src.base import get_session

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(good_router.router)


@app.on_event("startup")
async def feed_db():
    if not os.path.exists("logs"):
        os.mkdir("logs")
    await good_service.good_service.feed_data_in_db()
    # await good_service.good_service.get_all_goods(session)
