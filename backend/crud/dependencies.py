from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from database.config import async_session
from crud.user import UserCRUD
from crud.conciliation import ConciliationCRUD

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


# Dependency para el CRUD de conciliaciones
async def get_conciliation_crud() -> AsyncGenerator[ConciliationCRUD, None]:
    async with async_session() as session:
        async with session.begin():
            yield ConciliationCRUD(session)