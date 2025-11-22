from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from api import user, auth, me, conciliation
from database.config import engine, database, Base


app = FastAPI()

# CORS middleware DEBE estar ANTES de los routers
# IMPORTANTE: El orden importa - CORS debe ser el PRIMER middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],
    expose_headers=["*"],
    max_age=3600,
)

# Exception handler para asegurar que los headers CORS se agreguen incluso en errores
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Asegura que los headers CORS se agreguen en respuestas de error"""
    origin = request.headers.get("origin")
    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ]
    
    headers = {}
    if origin and origin in allowed_origins:
        headers["Access-Control-Allow-Origin"] = origin
        headers["Access-Control-Allow-Credentials"] = "true"
        headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept, Origin, X-Requested-With"
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=headers,
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Asegura que los headers CORS se agreguen en errores de validación"""
    origin = request.headers.get("origin")
    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ]
    
    headers = {}
    if origin and origin in allowed_origins:
        headers["Access-Control-Allow-Origin"] = origin
        headers["Access-Control-Allow-Credentials"] = "true"
        headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept, Origin, X-Requested-With"
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
        headers=headers,
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
