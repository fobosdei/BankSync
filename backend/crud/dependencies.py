from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from database.config import async_session
from crud.user import UserCRUD

# Dependency para la sesión de base de datos
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        async with session.begin():
            yield session

# Dependency para el CRUD de usuarios
async def get_user_crud() -> AsyncGenerator[UserCRUD, None]:
    async with async_session() as session:
        async with session.begin():
            yield UserCRUD(session)