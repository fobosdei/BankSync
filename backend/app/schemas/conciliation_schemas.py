from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ConciliationStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Transaction(BaseModel):
    fecha: str
    descripcion: str
    monto: float
    tipo: str
    referencia: Optional[str] = None


class ConciliationResult(BaseModel):
    conciliation_id: str
    status: str
    extracto_transactions: List[Dict[str, Any]]
    erp_transactions: List[Dict[str, Any]]
    matches: List[Dict[str, Any]]
    discrepancies: List[Dict[str, Any]]
    unmatched_extracto: List[Dict[str, Any]]
    unmatched_erp: List[Dict[str, Any]]
    summary: Dict[str, Any]
    created_at: str


class ConciliationRequest(BaseModel):
    extracto_data: List[Transaction]
    erp_data: List[Transaction]


class ReconciliationItem(BaseModel):
    id: str
    name: str
    status: str
    created_at: datetime
    summary: Dict[str, Any]

    class Config:
        from_attributes = True


class DashboardSummary(BaseModel):
    total_conciliaciones: int
    promedio_porcentaje_conciliado: float
    total_transacciones_pdf: int
    total_transacciones_excel: int
    total_discrepancias: int
    total_pendientes_pdf: int
    total_pendientes_erp: int
