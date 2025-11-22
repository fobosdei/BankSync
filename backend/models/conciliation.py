from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID

from database.config import Base


class UploadModel(Base):
    __tablename__ = "uploads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    original_filename = Column(Text, nullable=False)
    storage_path = Column(Text, nullable=False)
    status = Column(Text, nullable=False, default="uploaded")
    # Nota: no podemos usar el nombre de atributo "metadata" porque está reservado por SQLAlchemy.
    # Mantenemos el nombre de columna "metadata" en la BD para compatibilidad.
    upload_metadata = Column("metadata", JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )


class ReconciliationModel(Base):
    __tablename__ = "reconciliations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    upload_id = Column(UUID(as_uuid=True), ForeignKey("uploads.id"), nullable=False)
    name = Column(Text, nullable=False)
    status = Column(Text, nullable=False, default="draft")
    summary = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )


class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    upload_id = Column(UUID(as_uuid=True), ForeignKey("uploads.id"), nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(Text, nullable=False, default="USD")
    internal_reference = Column(Text, nullable=True)
    external_reference = Column(Text, nullable=True)
    raw_data = Column(JSONB, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

