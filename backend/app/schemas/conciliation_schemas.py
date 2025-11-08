from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

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
