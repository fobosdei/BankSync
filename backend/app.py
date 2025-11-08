from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import user, auth, me, conciliation
from database.config import engine, database, Base


app = FastAPI()

# CORS middleware must be added before routers
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

methods = [
    "DELETE",
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "OPTIONS",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=["*"],
)

# Add routers after middleware
app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(me.router, prefix="/api")
app.include_router(conciliation.router, prefix="/api")


@app.on_event("startup")
async def startup():
    await database.connect()
    # Don't create tables - they already exist in Supabase
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
