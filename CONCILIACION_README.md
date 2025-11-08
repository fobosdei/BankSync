# 🏦 Sistema de Conciliaciones Bancarias con IA

## ✅ Integración Completada

El sistema de conciliaciones bancarias con OpenAI ha sido integrado exitosamente en tu aplicación BankSync.

## 📁 Estructura Creada

```
backend/
├── app/
│   ├── services/
│   │   ├── openai_service.py          # Extracción de PDF con OpenAI
│   │   └── conciliation_service.py    # Lógica de conciliación
│   └── schemas/
│       └── conciliation_schemas.py    # Schemas de datos
├── api/
│   └── conciliation.py                # Endpoints REST API
└── .env.example                       # Ejemplo de configuración

frontend/
├── src/
│   ├── api/
│   │   └── conciliation.js            # Cliente API
│   └── components/
│       └── ConciliacionesContent.vue  # UI completa
```

## 🔧 Configuración Requerida

### 1. Agregar API Key de OpenAI

Edita tu archivo `backend/.env` y agrega:

```env
OPENAI_API_KEY=sk-tu-api-key-aqui
```

**¿Dónde obtener la API Key?**
1. Ve a https://platform.openai.com/api-keys
2. Crea una nueva API key
3. Cópiala y pégala en el `.env`

### 2. Verificar que el servidor esté corriendo

```bash
cd backend
python run.py --dev
```

El servidor debe estar en: `http://localhost:5001`

### 3. Verificar que el frontend esté corriendo

```bash
cd frontend
npm run dev
```

El frontend debe estar en: `http://localhost:5173`

## 🚀 Cómo Usar

### Desde la Interfaz Web:

1. **Inicia sesión** en la aplicación
2. Ve a la sección **"Conciliaciones"** en el menú lateral
3. Haz clic en el botón **"Conciliar todo con IA"** (botón morado)
4. **Sube los archivos:**
   - **PDF del extracto bancario** (hasta 10MB)
   - **Excel del ERP** con movimientos contables (hasta 10MB)
5. Haz clic en **"Procesar con IA"**
6. Espera mientras OpenAI procesa los archivos (puede tomar 10-30 segundos)
7. **Revisa los resultados:**
   - Coincidencias encontradas
   - Transacciones sin match del PDF
   - Transacciones sin match del ERP
   - Porcentaje de conciliación

### Formato del Excel del ERP:

El archivo Excel debe tener columnas con nombres como:
- `fecha` o `date` o `fecha_transaccion`
- `descripcion` o `concepto` o `detalle`
- `monto` o `valor` o `importe`
- `referencia` o `ref` o `numero` (opcional)

Ejemplo:

| fecha      | descripcion              | monto    | referencia |
|------------|--------------------------|----------|------------|
| 2025-10-10 | Transferencia Nómina     | 12500000 | TRF-001    |
| 2025-10-09 | Pago Proveedor ABC       | 3200000  | PAG-892    |

## 🔌 Endpoints API

### POST `/api/conciliation/conciliar`
Realiza la conciliación completa entre PDF y Excel.

**Headers:**
```
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

**Body:**
- `extracto_pdf`: Archivo PDF del extracto bancario
- `movimientos_excel`: Archivo Excel del ERP

**Response:**
```json
{
  "conciliation_id": "uuid",
  "status": "completed",
  "extracto_transactions": [...],
  "erp_transactions": [...],
  "matches": [...],
  "discrepancies": [...],
  "unmatched_extracto": [...],
  "unmatched_erp": [...],
  "summary": {
    "total_transacciones_pdf": 10,
    "total_transacciones_excel": 12,
    "coincidencias_encontradas": 8,
    "porcentaje_conciliado": 80.0
  }
}
```

### POST `/api/conciliation/probar-pdf`
Solo extrae transacciones del PDF (para pruebas).

**Headers:**
```
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

**Body:**
- `archivo_pdf`: Archivo PDF

### GET `/api/conciliation/health`
Verifica el estado del servicio.

**Response:**
```json
{
  "status": "healthy",
  "service": "Conciliaciones API",
  "openai_configured": true
}
```

## 🧪 Pruebas con Postman

### 1. Login
```
POST http://localhost:5001/api/auth/login
Content-Type: application/x-www-form-urlencoded

username=tu@email.com
password=tu_password
```

Copia el `access_token` de la respuesta.

### 2. Conciliar
```
POST http://localhost:5001/api/conciliation/conciliar
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

extracto_pdf: [seleccionar archivo PDF]
movimientos_excel: [seleccionar archivo Excel]
```

## 📊 Características

✅ **Extracción Inteligente con OpenAI**
- Extrae automáticamente transacciones de PDFs bancarios
- Identifica fecha, descripción, monto y tipo de transacción
- Maneja diferentes formatos de extractos

✅ **Conciliación Automática**
- Compara transacciones por fecha y monto
- Tolerancia de 5 centavos en diferencias
- Identifica coincidencias y discrepancias

✅ **Interfaz Moderna**
- Drag & drop para subir archivos
- Estados de procesamiento en tiempo real
- Visualización de resultados con estadísticas
- Tabla interactiva con todas las transacciones

✅ **Seguridad**
- Todos los endpoints requieren autenticación
- Archivos temporales se eliminan automáticamente
- Validación de tipos de archivo

## 🐛 Solución de Problemas

### Error: "No se encontró la API key de OpenAI"
**Solución:** Agrega `OPENAI_API_KEY` en el archivo `.env`

### Error: "401 Unauthorized"
**Solución:** Inicia sesión primero y usa el token en el header

### Error: "numpy.dtype size changed"
**Solución:** Ya resuelto. Numpy y pandas están actualizados.

### El PDF no se procesa correctamente
**Solución:** Asegúrate de que el PDF tenga texto extraíble (no sea una imagen escaneada)

## 📦 Dependencias Instaladas

```
openai==1.12.0
PyPDF2==3.0.1
pandas==2.3.3
openpyxl==3.1.2
numpy==2.3.4
```

## 💡 Próximos Pasos

1. **Agrega tu OPENAI_API_KEY** al archivo `.env`
2. **Prueba con archivos reales** de tu banco
3. **Ajusta la tolerancia** de conciliación si es necesario
4. **Exporta resultados** a Excel o PDF (próxima feature)

## 🎯 Flujo Completo

```
Usuario → Sube PDF + Excel → Frontend
                ↓
        API /conciliar → Backend
                ↓
        OpenAI extrae PDF → openai_service.py
                ↓
        Procesa Excel → conciliation_service.py
                ↓
        Compara y concilia → conciliation_service.py
                ↓
        Retorna resultados → Frontend
                ↓
        Muestra en tabla → ConciliacionesContent.vue
```

## 📞 Soporte

Si tienes problemas, verifica:
1. ✅ Backend corriendo en puerto 5001
2. ✅ Frontend corriendo en puerto 5173
3. ✅ OPENAI_API_KEY configurada
4. ✅ Usuario autenticado
5. ✅ Archivos en formato correcto

---

**¡Todo listo para usar! 🚀**
