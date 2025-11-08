import pandas as pd
from typing import List, Dict, Any, Tuple
from datetime import datetime
import uuid

class ConciliationService:
    def __init__(self):
        self.results = {}
    
    def process_excel(self, excel_path: str) -> List[Dict]:
        """Procesar archivo Excel del ERP y convertirlo a transacciones"""
        try:
            df = pd.read_excel(excel_path)
            transacciones = []
            
            # Mapeo flexible de columnas
            for _, row in df.iterrows():
                # Buscar columnas comunes
                fecha = self._buscar_valor(row, ['fecha', 'date', 'fecha_transaccion'])
                descripcion = self._buscar_valor(row, ['descripcion', 'concepto', 'detalle', 'description'])
                monto = self._buscar_valor(row, ['monto', 'valor', 'importe', 'amount'])
                referencia = self._buscar_valor(row, ['referencia', 'ref', 'numero', 'id'])
                
                # Determinar tipo basado en el monto
                try:
                    monto_float = float(monto) if monto else 0.0
                    tipo = "ingreso" if monto_float >= 0 else "gasto"
                    
                    # NORMALIZAR FECHA - Convertir al mismo formato que el PDF
                    fecha_normalizada = self._normalizar_fecha_excel(fecha)
                    
                    transaction = {
                        "fecha": fecha_normalizada,  # Usar fecha normalizada
                        "descripcion": str(descripcion),
                        "monto": abs(monto_float),
                        "tipo": tipo,
                        "referencia": str(referencia) if referencia else None
                    }
                    transacciones.append(transaction)
                except ValueError:
                    continue
            
            return transacciones
            
        except Exception as e:
            raise Exception(f"Error procesando Excel: {str(e)}")
    
    def _normalizar_fecha_excel(self, fecha_raw):
        """Normalizar fecha del Excel al formato YYYY-MM-DD"""
        try:
            # Si es string, limpiarlo
            if isinstance(fecha_raw, str):
                # Extraer solo la parte de la fecha (antes del espacio si tiene hora)
                fecha_parte = fecha_raw.split(' ')[0]
                # Convertir a datetime
                fecha_dt = pd.to_datetime(fecha_parte, errors='coerce')
                if pd.isna(fecha_dt):
                    return str(fecha_raw)
                return fecha_dt.strftime('%Y-%m-%d')
            
            # Si es datetime de pandas o Python
            elif hasattr(fecha_raw, 'strftime'):
                return fecha_raw.strftime('%Y-%m-%d')
            
            # Si es numpy datetime64
            elif 'datetime64' in str(type(fecha_raw)):
                return pd.to_datetime(fecha_raw).strftime('%Y-%m-%d')
            
            # Por defecto, convertir a string
            else:
                return str(fecha_raw)
                
        except Exception as e:
            print(f"⚠️  Error normalizando fecha {fecha_raw}: {e}")
            return str(fecha_raw)
    
    def _buscar_valor(self, row, posibles_nombres):
        """Buscar valor en una fila por posibles nombres de columna"""
        for nombre in posibles_nombres:
            if nombre in row:
                return row[nombre]
        return ""
    
    def conciliar(self, transacciones_pdf: List[Dict], transacciones_excel: List[Dict]) -> Dict:
        """Realizar la conciliación entre ambas fuentes"""
        
        # Convertir transacciones PDF al formato estándar
        pdf_standard = self._convertir_a_estandar(transacciones_pdf)
        
        # Algoritmo de matching
        matches, discrepancies, unmatched_pdf, unmatched_excel = self._encontrar_coincidencias(
            pdf_standard, transacciones_excel
        )
        
        # Crear resumen
        summary = self._crear_resumen(
            pdf_standard, transacciones_excel, matches, discrepancies, unmatched_pdf, unmatched_excel
        )
        
        resultado = {
            "conciliation_id": str(uuid.uuid4()),
            "status": "completed",
            "extracto_transactions": pdf_standard,
            "erp_transactions": transacciones_excel,
            "matches": matches,
            "discrepancies": discrepancies,
            "unmatched_extracto": unmatched_pdf,
            "unmatched_erp": unmatched_excel,
            "summary": summary,
            "created_at": datetime.now().isoformat()
        }
        
        return resultado
    
    def _convertir_a_estandar(self, transacciones_pdf: List[Dict]) -> List[Dict]:
        """Convertir transacciones extraídas por OpenAI al formato estándar"""
        estandar = []
        
        # Palabras clave para clasificar transacciones
        palabras_gasto = ['pago', 'seguro', 'comision', 'servicio', 'impuesto', 'retencion', 
                         'debito', 'retiro', 'cuota', 'gasto', 'agencias', 'agencia']
        palabras_ingreso = ['deposito', 'venta', 'cobro', 'transferencia', 'ingreso', 
                           'abono', 'reembolso', 'interes']
        
        for i, trans in enumerate(transacciones_pdf):
            try:
                fecha = trans.get('fecha', '')
                descripcion = trans.get('descripcion', '').lower()
                
                # Obtener monto y convertir a positivo
                monto_raw = trans.get('monto') or trans.get('valor') or 0
                monto_float = abs(float(monto_raw))
                
                # Determinar tipo basado en descripción (sobreescribir lo que diga OpenAI)
                tipo = trans.get('tipo', '').lower()
                
                # Si la descripción contiene palabras de gasto, forzar a gasto
                if any(palabra in descripcion for palabra in palabras_gasto):
                    tipo = "gasto"
                elif any(palabra in descripcion for palabra in palabras_ingreso):
                    tipo = "ingreso"
                # Si no se puede determinar, usar lo que dijo OpenAI
                elif tipo not in ['ingreso', 'gasto']:
                    tipo = "gasto"  # Por defecto asumir gasto si no está claro
                
                transaction = {
                    "fecha": str(fecha),
                    "descripcion": trans.get('descripcion', ''),  # Original en mayúsculas
                    "monto": monto_float,
                    "tipo": tipo,
                    "referencia": f"PDF_{i}"
                }
                estandar.append(transaction)
                
                print(f"✅ Transacción {i}: {descripcion} → {tipo} (${monto_float})")
                
            except Exception as e:
                print(f"⚠️  Error convirtiendo transacción {i}: {e}")
                print(f"   Transacción original: {trans}")
                continue
        
        return estandar
    
    def _encontrar_coincidencias(self, pdf_trans: List[Dict], excel_trans: List[Dict]) -> Tuple:
        """Encontrar coincidencias entre las transacciones"""
        matches = []
        discrepancies = []
        unmatched_pdf = pdf_trans.copy()
        unmatched_excel = excel_trans.copy()
        
        # Algoritmo de matching por monto y fecha
        for trans_pdf in pdf_trans[:]:
            for trans_excel in excel_trans[:]:
                if self._es_coincidencia(trans_pdf, trans_excel):
                    match_info = {
                        "pdf_transaction": trans_pdf,
                        "excel_transaction": trans_excel,
                        "confidence": 0.95
                    }
                    
                    # Verificar discrepancias
                    if abs(trans_pdf['monto'] - trans_excel['monto']) > 0.01:
                        discrepancy = {
                            "pdf_transaction": trans_pdf,
                            "excel_transaction": trans_excel,
                            "issue": f"Diferencia de monto: PDF=${trans_pdf['monto']:.2f} vs Excel=${trans_excel['monto']:.2f}",
                            "difference": abs(trans_pdf['monto'] - trans_excel['monto'])
                        }
                        discrepancies.append(discrepancy)
                    
                    matches.append(match_info)
                    if trans_pdf in unmatched_pdf:
                        unmatched_pdf.remove(trans_pdf)
                    if trans_excel in unmatched_excel:
                        unmatched_excel.remove(trans_excel)
                    break
        
        return matches, discrepancies, unmatched_pdf, unmatched_excel
    
    def _es_coincidencia(self, trans1: Dict, trans2: Dict) -> bool:
        """Determinar si dos transacciones coinciden"""
        # Coincidencia por monto (con tolerancia) y fecha
        coincidencia_monto = abs(trans1['monto'] - trans2['monto']) < 0.05  # 5 centavos tolerancia
        coincidencia_fecha = trans1['fecha'] == trans2['fecha']  # Ahora las fechas están normalizadas
        
        return coincidencia_monto and coincidencia_fecha
    
    def _crear_resumen(self, pdf_trans, excel_trans, matches, discrepancies, unmatched_pdf, unmatched_excel):
        """Crear resumen de la conciliación"""
        total_pdf = sum(t['monto'] for t in pdf_trans)
        total_excel = sum(t['monto'] for t in excel_trans)
        
        return {
            "total_transacciones_pdf": len(pdf_trans),
            "total_transacciones_excel": len(excel_trans),
            "coincidencias_encontradas": len(matches),
            "discrepancies": len(discrepancies),
            "transacciones_sin_match_pdf": len(unmatched_pdf),
            "transacciones_sin_match_excel": len(unmatched_excel),
            "total_monto_pdf": total_pdf,
            "total_monto_excel": total_excel,
            "diferencia_total": abs(total_pdf - total_excel),
            "porcentaje_conciliado": (len(matches) / max(len(pdf_trans), len(excel_trans))) * 100 if pdf_trans or excel_trans else 0
        }
