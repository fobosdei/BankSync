from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

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
            metadata=metadata or {},
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
        upload_id: UUID,
        name: str,
        status: str,
        summary: Dict[str, Any],
    ) -> ReconciliationModel:
        reconciliation = ReconciliationModel(
            id=uuid4(),
            upload_id=upload_id,
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
        upload_metadata = {
            "pdf_filename": pdf_filename,
            "excel_filename": excel_filename,
            "summary": result_summary,
            "stored_files": {
                "pdf": pdf_file_path,
                "excel": excel_file_path,
            },
        }

        upload = await self.create_upload(
            user_id=user_id,
            original_filename=f"{pdf_filename} | {excel_filename}",
            storage_path=storage_path,
            status="processed",
            metadata=upload_metadata,
        )

        await self.create_transactions_for_upload(upload.id, pdf_transactions, "pdf")
        await self.create_transactions_for_upload(upload.id, excel_transactions, "erp")

        reconciliation = await self.create_reconciliation(
            upload_id=upload.id,
            name=f"Conciliación - {pdf_filename}",
            status="completed",
            summary=result_summary,
        )

        await self.db_session.flush()

        return reconciliation

