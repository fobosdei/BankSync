# Análisis de Schema de Base de Datos - BankSync

## Resumen Ejecutivo

Este documento compara el schema SQL (`BDBanksSyncSchema.sql`) con los modelos SQLAlchemy y el código que los utiliza, identificando inconsistencias y áreas de mejora.

---

## ✅ Tablas que Coinciden Correctamente

### 1. **`uploads`** ✅
- **Schema SQL**: `id`, `user_id`, `original_filename`, `storage_path`, `status`, `metadata`, `created_at`, `updated_at`
- **Modelo SQLAlchemy** (`UploadModel`): Todos los campos coinciden
- **Nota**: El modelo usa `upload_metadata` como atributo Python (porque `metadata` está reservado en SQLAlchemy), pero mapea correctamente a la columna `metadata` en la BD.

### 2. **`reconciliations`** ✅
- **Schema SQL**: `id`, `upload_id`, `name`, `status`, `summary`, `created_at`, `updated_at`
- **Modelo SQLAlchemy** (`ReconciliationModel`): Todos los campos coinciden perfectamente.

### 3. **`transactions`** ✅
- **Schema SQL**: `id`, `upload_id`, `amount`, `currency`, `internal_reference`, `external_reference`, `raw_data`, `created_at`, `updated_at`
- **Modelo SQLAlchemy** (`TransactionModel`): Todos los campos coinciden perfectamente.

---

## ⚠️ Problemas Encontrados

### 1. **Tabla `users`** - Inconsistencias

**Schema SQL tiene:**
```sql
- id (uuid)
- email (text)
- full_name (text)
- role (text, default 'viewer')
- metadata (jsonb, default '{}')
- created_at (timestamp)
- updated_at (timestamp)
```

**Modelo SQLAlchemy (`UserModels`) tiene:**
```python
- id ✅
- email ✅
- full_name ✅
- password_hash ❌ (NO está en schema SQL)
- role ✅ (pero default es 'user' en modelo, 'viewer' en schema)
- extra ❌ (NO está en schema SQL, debería ser 'metadata')
- created_at ✅
- updated_at ✅
- last_login ❌ (NO está en schema SQL)
```

**Problemas:**
1. El modelo usa `password_hash` pero el schema SQL no lo tiene. Esto es crítico para autenticación.
2. El modelo usa `extra` pero el schema tiene `metadata`.
3. El modelo tiene `last_login` pero el schema no lo tiene.
4. El default de `role` difiere: modelo usa `'user'`, schema usa `'viewer'`.

**Recomendación:**
- Agregar `password_hash` al schema SQL (es necesario para autenticación).
- Cambiar `extra` en el modelo a `metadata` para coincidir con el schema.
- Agregar `last_login` al schema SQL si se necesita tracking de sesiones.
- Unificar el default de `role` (recomendado: `'viewer'` en ambos).

### 2. **Tabla `reports`** - Modelo Faltante

**Schema SQL tiene:**
```sql
- id (uuid)
- reconciliation_id (uuid, FK a reconciliations)
- title (text)
- storage_path (text)
- metadata (jsonb, default '{}')
- created_at (timestamp)
- updated_at (timestamp)
```

**Modelo SQLAlchemy:** ❌ NO EXISTE

**Recomendación:**
- Crear `ReportModel` en `models/report.py` si se va a usar la funcionalidad de reportes.

### 3. **Tabla `logs`** - Modelo Faltante

**Schema SQL tiene:**
```sql
- id (uuid)
- user_id (uuid, FK a users, nullable)
- service_name (text)
- action (text)
- message (text)
- properties (jsonb, default '{}')
- created_at (timestamp)
- updated_at (timestamp)
```

**Modelo SQLAlchemy:** ❌ NO EXISTE

**Recomendación:**
- Crear `LogModel` en `models/log.py` si se necesita auditoría/logging estructurado.

### 4. **Tabla `workflows`** - Modelo Faltante

**Schema SQL tiene:**
```sql
- id (uuid)
- name (text)
- description (text, nullable)
- is_active (boolean, default true)
- metadata (jsonb, default '{}')
- created_at (timestamp)
- updated_at (timestamp)
```

**Modelo SQLAlchemy:** ❌ NO EXISTE

**Recomendación:**
- Crear `WorkflowModel` en `models/workflow.py` si se va a usar n8n o automatización.

---

## 🔧 Correcciones Aplicadas

### 1. **Corrección en `crud/conciliation.py`**
- **Línea 34**: Cambiado `metadata=metadata or {}` → `upload_metadata=metadata or {}`
- **Razón**: El modelo `UploadModel` usa `upload_metadata` como nombre de atributo (mapea a columna `metadata` en BD).

---

## 📋 Checklist de Verificación

- [x] `uploads` - Modelo y schema coinciden
- [x] `reconciliations` - Modelo y schema coinciden
- [x] `transactions` - Modelo y schema coinciden
- [ ] `users` - **REQUIERE CORRECCIÓN** (ver sección de problemas)
- [ ] `reports` - **FALTA MODELO** (crear si se usa)
- [ ] `logs` - **FALTA MODELO** (crear si se usa)
- [ ] `workflows` - **FALTA MODELO** (crear si se usa)

---

## 🎯 Próximos Pasos Recomendados

1. **Corregir modelo `UserModels`**:
   - Agregar `password_hash` al schema SQL.
   - Cambiar `extra` → `metadata` en el modelo.
   - Agregar `last_login` al schema SQL.
   - Unificar default de `role`.

2. **Crear modelos faltantes** (si se van a usar):
   - `ReportModel` para reportes generados.
   - `LogModel` para auditoría.
   - `WorkflowModel` para automatización con n8n.

3. **Verificar Foreign Keys**:
   - Todas las FK en el schema SQL están correctamente definidas.
   - Los modelos SQLAlchemy usan `ForeignKey()` correctamente.

4. **Índices**:
   - El schema SQL no define índices explícitos (excepto PKs).
   - Los modelos SQLAlchemy definen `index=True` en `user_id` de `uploads` y `email` de `users`.
   - Considerar agregar índices en el schema SQL para mejor performance.

---

## 📝 Notas Adicionales

- El schema SQL usa `gen_random_uuid()` para defaults de UUID, que es compatible con PostgreSQL/Supabase.
- Los modelos SQLAlchemy usan `uuid4()` de Python, que también genera UUIDs válidos.
- Todos los campos `timestamp with time zone` en el schema coinciden con `DateTime(timezone=True)` en SQLAlchemy.
- Los campos `jsonb` en el schema coinciden con `JSONB` en SQLAlchemy.

---

**Última actualización**: 2025-01-XX
**Revisado por**: AI Assistant
