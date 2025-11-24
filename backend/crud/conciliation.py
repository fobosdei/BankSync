from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.conciliation import (
    ReconciliationModel,
    TransactionModel,
    UploadModel,
)


class ConciliationCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_upload(
        self,
        *,
        user_id: UUID,
        original_filename: str,
        storage_path: str,
        status: str = "processed",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> UploadModel:
        upload = UploadModel(
            id=uuid4(),
            user_id=user_id,
            original_filename=original_filename,
            storage_path=storage_path,
            status=status,
            upload_metadata=metadata or {},  # ✅ CORREGIDO: era "metadata"
        )
        self.db_session.add(upload)
        await self.db_session.flush()
        await self.db_session.refresh(upload)
        return upload

    async def create_transactions_for_upload(
        self, upload_id: UUID, transactions: List[Dict[str, Any]], source: str
    ) -> None:
        for entry in transactions:
            amount = entry.get("monto") or entry.get("amount") or entry.get("valor")
            if amount is None:
                continue
            try:
                amount_decimal = Decimal(str(amount))
            except (InvalidOperation, TypeError, ValueError):
                continue
            record_data = dict(entry)
            record_data.setdefault("source", source)

            transaction = TransactionModel(
                id=uuid4(),
                upload_id=upload_id,
                amount=amount_decimal,
                currency=entry.get("currency", "COP"),
                internal_reference=entry.get("referencia"),
                external_reference=entry.get("external_reference"),
                raw_data=record_data,
            )
            self.db_session.add(transaction)

    async def create_reconciliation(
        self,
        *,
        pdf_upload_id: UUID,  # ✅ CORREGIDO: era "upload_id"
        excel_upload_id: UUID,  # ✅ AGREGADO
        user_id: UUID,  # ✅ AGREGADO
        name: str,
        status: str,
        summary: Dict[str, Any],
    ) -> ReconciliationModel:
        reconciliation = ReconciliationModel(
            id=uuid4(),
            pdf_upload_id=pdf_upload_id,  # ✅ CORREGIDO
            excel_upload_id=excel_upload_id,  # ✅ AGREGADO
            user_id=user_id,  # ✅ AGREGADO
            name=name,
            status=status,
            summary=summary,
        )
        self.db_session.add(reconciliation)
        await self.db_session.flush()
        await self.db_session.refresh(reconciliation)
        return reconciliation

    async def persist_conciliation_result(
        self,
        *,
        user_id: UUID,
        storage_path: str,
        pdf_filename: str,
        excel_filename: str,
        pdf_file_path: str,
        excel_file_path: str,
        pdf_transactions: List[Dict[str, Any]],
        excel_transactions: List[Dict[str, Any]],
        result_summary: Dict[str, Any],
    ) -> ReconciliationModel:
        # ✅ CORREGIDO: Crear uploads separados para PDF y Excel
        pdf_upload = await self.create_upload(
            user_id=user_id,
            original_filename=pdf_filename,
            storage_path=f"{storage_path}/{pdf_filename}",
            status="processed",
            metadata={
                "type": "pdf",
                "stored_file": pdf_file_path,
            },
        )

        excel_upload = await self.create_upload(
            user_id=user_id,
            original_filename=excel_filename,
            storage_path=f"{storage_path}/{excel_filename}",
            status="processed",
            metadata={
                "type": "excel",
                "stored_file": excel_file_path,
            },
        )

        # Crear transacciones para cada upload
        await self.create_transactions_for_upload(pdf_upload.id, pdf_transactions, "pdf")
        await self.create_transactions_for_upload(excel_upload.id, excel_transactions, "erp")

        # ✅ CORREGIDO: Usar ambos upload_id
        reconciliation = await self.create_reconciliation(
            pdf_upload_id=pdf_upload.id,  # ✅ CORREGIDO
            excel_upload_id=excel_upload.id,  # ✅ AGREGADO
            user_id=user_id,  # ✅ AGREGADO
            name=f"Conciliación - {pdf_filename}",
            status="completed",
            summary=result_summary,
        )

        await self.db_session.flush()

        return reconciliation

    async def list_recent_reconciliations(
        self, limit: int = 20
    ) -> List[ReconciliationModel]:
        """
        Obtener las conciliaciones más recientes para mostrarlas en historial/reportes.
        """
        stmt = (
            select(ReconciliationModel)
            .order_by(ReconciliationModel.created_at.desc())
            .limit(limit)
        )
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_dashboard_summary(self) -> Dict[str, Any]:
        """
        Construir un resumen simple para el dashboard a partir de las conciliaciones.
        Usa los campos agregados del JSON `summary` para no recalcular todo.
        """
        stmt = select(ReconciliationModel.summary)
        result = await self.db_session.execute(stmt)
        summaries = [row or {} for row in result.scalars().all()]

        if not summaries:
            return {
                "total_conciliaciones": 0,
                "promedio_porcentaje_conciliado": 0.0,
                "total_transacciones_pdf": 0,
                "total_transacciones_excel": 0,
                "total_discrepancias": 0,
                "total_pendientes_pdf": 0,
                "total_pendientes_erp": 0,
            }

        total_conciliaciones = len(summaries)
        sum_porcentaje = 0.0
        total_pdf = 0
        total_excel = 0
        total_discrepancias = 0
        total_pendientes_pdf = 0
        total_pendientes_erp = 0

        for s in summaries:
            sum_porcentaje += float(s.get("porcentaje_conciliado", 0) or 0)
            total_pdf += int(s.get("total_transacciones_pdf", 0) or 0)
            total_excel += int(s.get("total_transacciones_excel", 0) or 0)
            total_discrepancias += int(s.get("discrepancies", 0) or 0)
            total_pendientes_pdf += int(s.get("transacciones_sin_match_pdf", 0) or 0)
            total_pendientes_erp += int(s.get("transacciones_sin_match_excel", 0) or 0)

        promedio_porcentaje = sum_porcentaje / total_conciliaciones

        return {
            "total_conciliaciones": total_conciliaciones,
            "promedio_porcentaje_conciliado": promedio_porcentaje,
            "total_transacciones_pdf": total_pdf,
            "total_transacciones_excel": total_excel,
            "total_discrepancias": total_discrepancias,
            "total_pendientes_pdf": total_pendientes_pdf,
            "total_pendientes_erp": total_pendientes_erp,
        }

    async def get_transactions(
        self,
        user_id: Optional[UUID] = None,
        upload_id: Optional[UUID] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[TransactionModel]:
        """
        Obtener transacciones con filtros opcionales.
        """
        stmt = select(TransactionModel)
        
        # Filtrar por upload_id si se proporciona
        if upload_id:
            stmt = stmt.where(TransactionModel.upload_id == upload_id)
        elif user_id:
            # Si se proporciona user_id, filtrar por uploads del usuario
            # Necesitamos hacer join con UploadModel para filtrar por user_id
            stmt = stmt.join(
                UploadModel, 
                TransactionModel.upload_id == UploadModel.id
            ).where(UploadModel.user_id == user_id)
        
        stmt = stmt.order_by(TransactionModel.created_at.desc()).limit(limit).offset(offset)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_unique_banks_from_uploads(self, user_id: UUID) -> List[str]:
        """
        Extraer nombres únicos de bancos desde los metadatos de uploads.
        """
        stmt = select(UploadModel.upload_metadata).where(UploadModel.user_id == user_id)
        result = await self.db_session.execute(stmt)
        metadata_list = result.scalars().all()
        
        banks = set()
        for metadata in metadata_list:
            if metadata and isinstance(metadata, dict):
                bank_name = metadata.get("bank_name") or metadata.get("banco")
                if bank_name:
                    banks.add(str(bank_name))
        
        return sorted(list(banks))
