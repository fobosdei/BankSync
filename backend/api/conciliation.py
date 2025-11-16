from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
import tempfile
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Import services directly
try:
    from app.services.openai_service import OpenAIBankExtractor
    from app.services.conciliation_service import ConciliationService
    from app.schemas.conciliation_schemas import (
        ConciliationResult,
        ReconciliationItem,
        DashboardSummary,
    )
except ImportError:
    # Fallback a imports absolutos usando importlib
    import importlib.util

    # Cargar openai_service
    openai_path = backend_dir / "app" / "services" / "openai_service.py"
    spec = importlib.util.spec_from_file_location("openai_service", openai_path)
    openai_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(openai_module)
    OpenAIBankExtractor = openai_module.OpenAIBankExtractor

    # Cargar conciliation_service
    conciliation_path = backend_dir / "app" / "services" / "conciliation_service.py"
    spec = importlib.util.spec_from_file_location("conciliation_service", conciliation_path)
    conciliation_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conciliation_module)
    ConciliationService = conciliation_module.ConciliationService

    # Para los esquemas usamos dict como fallback sencillo
    ConciliationResult = dict
    ReconciliationItem = dict
    DashboardSummary = dict

from auth.action import get_current_user
from schemas.user import UserResponse
from crud.dependencies import get_conciliation_crud
from crud.conciliation import ConciliationCRUD

router = APIRouter(prefix="/conciliation", tags=["conciliation"])

# Inicializar servicios (lazy loading)
openai_extractor = None
conciliation_service = None

def get_services():
    global openai_extractor, conciliation_service
    if openai_extractor is None:
        openai_extractor = OpenAIBankExtractor()
    if conciliation_service is None:
        conciliation_service = ConciliationService()
    return openai_extractor, conciliation_service


@router.post("/conciliar")
async def conciliar_archivos(
    extracto_pdf: UploadFile = File(...),
    movimientos_excel: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_user),
    conciliation_crud: ConciliationCRUD = Depends(get_conciliation_crud),
):
    """
    Endpoint principal que recibe ambos archivos y realiza la conciliación completa.
    Requiere autenticación.
    """
    try:
        # Validar archivos
        if not extracto_pdf.filename.endswith('.pdf'):
            raise HTTPException(400, "El extracto debe ser PDF")
        
        if not movimientos_excel.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(400, "Los movimientos deben ser Excel")
        
        print(f"📁 Usuario: {current_user.email}")
        print(f"📁 Procesando: {extracto_pdf.filename} y {movimientos_excel.filename}")
        
        # Guardar archivos temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as pdf_temp:
            pdf_temp.write(await extracto_pdf.read())
            pdf_path = pdf_temp.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as excel_temp:
            excel_temp.write(await movimientos_excel.read())
            excel_path = excel_temp.name
        
        try:
            # Obtener servicios
            extractor, conciliator = get_services()
            
            # Extraer transacciones del PDF usando OpenAI
            print("🔍 Extrayendo transacciones del PDF con OpenAI...")
            transacciones_pdf = extractor.process_pdf(pdf_path)
            
            # Procesar Excel del ERP
            print("📊 Procesando archivo Excel del ERP...")
            transacciones_excel = conciliator.process_excel(excel_path)
            
            # Realizar conciliación
            print("🔄 Realizando conciliación...")
            resultado = conciliator.conciliar(transacciones_pdf, transacciones_excel)

            # Persistir resultado en la base de datos (Supabase)
            try:
                reconciliation = await conciliation_crud.persist_conciliation_result(
                    user_id=current_user.id,
                    storage_path="supabase://banksync/uploads",
                    pdf_filename=extracto_pdf.filename,
                    excel_filename=movimientos_excel.filename,
                    pdf_file_path=pdf_path,
                    excel_file_path=excel_path,
                    pdf_transactions=transacciones_pdf,
                    excel_transactions=transacciones_excel,
                    result_summary=resultado["summary"],
                )
                resultado["reconciliation_id"] = str(reconciliation.id)
            except Exception as db_error:
                # No romper la experiencia del usuario si falla la persistencia
                print(f"⚠ Error guardando conciliación en BD: {db_error}")
            
            print(f"✅ Conciliación completada: {resultado['summary']['coincidencias_encontradas']} coincidencias")
            
            return resultado
            
        finally:
            # Limpiar archivos temporales
            os.unlink(pdf_path)
            os.unlink(excel_path)
        
    except Exception as e:
        print(f"❌ Error en conciliación: {str(e)}")
        raise HTTPException(500, f"Error en conciliación: {str(e)}")


@router.post("/probar-pdf")
async def probar_pdf(
    archivo_pdf: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Endpoint solo para probar la extracción de PDF.
    Requiere autenticación.
    """
    try:
        if not archivo_pdf.filename.endswith('.pdf'):
            raise HTTPException(400, "El archivo debe ser PDF")
            
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(await archivo_pdf.read())
            pdf_path = temp_file.name
        
        extractor, _ = get_services()
        transacciones = extractor.process_pdf(pdf_path)
        os.unlink(pdf_path)
        
        return {
            "success": True,
            "user": current_user.email,
            "transacciones_extraidas": len(transacciones),
            "data": transacciones
        }
    
    except Exception as e:
        raise HTTPException(500, f"Error probando PDF: {str(e)}")


@router.get("/historial", response_model=List[ReconciliationItem])
async def listar_conciliaciones(
    current_user: UserResponse = Depends(get_current_user),
    conciliation_crud: ConciliationCRUD = Depends(get_conciliation_crud),
):
    """
    Devuelve las conciliaciones más recientes del usuario actual para mostrar en
    historial, reportes o dashboard.
    """
    reconciliations = await conciliation_crud.list_recent_reconciliations()
    # Por simplicidad, por ahora no filtramos por usuario: asumimos un tenant
    return [
        ReconciliationItem(
            id=str(rec.id),
            name=rec.name,
            status=rec.status,
            created_at=rec.created_at,
            summary=rec.summary or {},
        )
        for rec in reconciliations
    ]


@router.get("/dashboard-resumen", response_model=DashboardSummary)
async def dashboard_resumen(
    current_user: UserResponse = Depends(get_current_user),
    conciliation_crud: ConciliationCRUD = Depends(get_conciliation_crud),
):
    """
    Resumen agregado para el dashboard principal.
    """
    summary_dict = await conciliation_crud.get_dashboard_summary()
    return DashboardSummary(**summary_dict)


@router.get("/health")
async def health_check():
    """Verificar estado del servicio de conciliación"""
    return {
        "status": "healthy", 
        "service": "Conciliaciones API",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY"))
    }
