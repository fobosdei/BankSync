from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import get_password_hash
from models.user import UserModels
from schemas import user as user_schema


class UserCRUD:
    db_session = None

    def __init__(self, db_session: AsyncSession = None):
        self.db_session = db_session

    async def get_user_by_email(self, email: str):
        stmt = select(UserModels).where(UserModels.email == email)
        result = await self.db_session.execute(stmt)
        return result.scalars().first()

    async def get_user_by_id(self, user_id: UUID):
        stmt = select(UserModels).where(UserModels.id == user_id)
        result = await self.db_session.execute(stmt)
        return result.scalars().first()

    async def get_users(self) -> List[user_schema.UserResponse]:
        stmt = select(UserModels)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def create_user(self, user: user_schema.UserRegister) -> UserModels:
        db_user = UserModels()
        db_user.email = user.email
        db_user.password_hash = get_password_hash(user.password)
        db_user.full_name = user.full_name
        db_user.role = user.role

        self.db_session.add(db_user)
        await self.db_session.flush()
        await self.db_session.refresh(db_user)
        return db_user

    async def update_user_login(self, email: str):
        db_user = await self.get_user_by_email(email)
        if not db_user:
            return None
        db_user.last_login = datetime.utcnow()
        await self.db_session.flush()
        await self.db_session.refresh(db_user)
        return db_user

    async def update_user(self, email: str, user_update: user_schema.UserUpdate):
        stmt = (
            update(UserModels)
            .where(UserModels.email == email)
            .values(**user_update.model_dump(exclude_unset=True))
        )
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)

    async def update_user_by_id(self, user_id: UUID, user_update: user_schema.UserUpdate):
        stmt = (
            update(UserModels)
            .where(UserModels.id == user_id)
            .values(**user_update.model_dump(exclude_unset=True))
        )
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)

    async def update_password(self, email: str, password: str):
        stmt = (
            update(UserModels)
            .where(UserModels.email == email)
            .values(password_hash=get_password_hash(password))
        )
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)

    async def deactivate_user_by_id(self, user_id: UUID):
        """
        Desactivar un usuario sin borrarlo: se marca su rol como 'inactive'.
        """
        stmt = (
            update(UserModels)
            .where(UserModels.id == user_id)
            .values(role="inactive")
        )
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)

    async def delete_user(self, email: str):
        stmt = delete(UserModels).where(UserModels.email == email)
        stmt.execution_options(synchronize_session="fetch")
        await self.db_session.execute(stmt)
