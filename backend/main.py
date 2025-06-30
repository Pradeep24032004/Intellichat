"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from .utils import dbAdaptor
from .routers import users, messages

db = dbAdaptor.DBAdaptor()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_room()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users.router)
app.include_router(messages.router)
"""

# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from .utils import dbAdaptor
from .routers import users, messages

db = dbAdaptor.DBAdaptor()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_room()
    yield

app = FastAPI(lifespan=lifespan)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pass db instance to routers
app.include_router(users.get_router(db))
app.include_router(messages.get_router(db))

