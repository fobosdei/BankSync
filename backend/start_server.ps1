# Script para iniciar el servidor FastAPI
# Uso: .\start_server.ps1

# Cambiar al directorio del backend
Set-Location $PSScriptRoot

# Activar el entorno virtual
if (Test-Path ".\Venv\Scripts\Activate.ps1") {
    Write-Host "Activando entorno virtual..." -ForegroundColor Green
    & ".\Venv\Scripts\Activate.ps1"
} else {
    Write-Host "ERROR: No se encontró el entorno virtual en .\Venv\Scripts\" -ForegroundColor Red
    exit 1
}

# Verificar que uvicorn está instalado
Write-Host "Verificando uvicorn..." -ForegroundColor Green
$uvicornPath = ".\Venv\Scripts\uvicorn.exe"
if (-not (Test-Path $uvicornPath)) {
    Write-Host "ERROR: uvicorn no está instalado. Ejecuta: pip install uvicorn" -ForegroundColor Red
    exit 1
}

# Iniciar el servidor
Write-Host "Iniciando servidor FastAPI en http://localhost:5001..." -ForegroundColor Green
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
& ".\Venv\Scripts\python.exe" -m uvicorn app:app --reload --host 0.0.0.0 --port 5001

