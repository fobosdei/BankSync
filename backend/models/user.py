from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB

from database.config import Base


# Create User class matching Supabase schema
class UserModels(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(Text, unique=True, nullable=False, index=True)
    full_name = Column(Text, nullable=True)
    password_hash = Column(Text, nullable=True)  # Nullable inicialmente para migración
    role = Column(Text, default="viewer")  # Coincide con schema SQL
    # Nota: 'metadata' está reservado en SQLAlchemy, pero mapeamos a la columna 'metadata' en BD
    user_metadata = Column("metadata", JSONB, nullable=True, default=dict)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<UserModels(id={self.id}, email={self.email}, full_name={self.full_name})>"
