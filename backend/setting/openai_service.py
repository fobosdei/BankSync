"""
Servicio para extraer transacciones bancarias de PDFs usando OpenAI
"""
from openai import OpenAI
import os
import json
import csv
from typing import List, Dict, Optional
import PyPDF2
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

class OpenAIBankExtractor:
    """
    Clase para extraer y procesar transacciones bancarias de PDFs
    usando la API de OpenAI
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el cliente de OpenAI
        
        Args:
            api_key: API key de OpenAI. Si no se proporciona, se lee de variable de entorno
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("No se encontró la API key de OpenAI")
        
        self.client = OpenAI(api_key=self.api_key)
    
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extrae el texto de un PDF
        
        Args:
            pdf_path: Ruta del archivo PDF
            
        Returns:
            Texto extraído del PDF
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                return text
        
        except Exception as e:
            raise Exception(f"Error al leer el PDF: {str(e)}")
    
    
    def extract_transactions_from_text(self, text: str) -> List[Dict]:
        """
        Usa OpenAI para extraer transacciones del texto del PDF
        
        Args:
            text: Texto extraído del PDF
            
        Returns:
            Lista de diccionarios con las transacciones
        """
        
        prompt = f"""
Eres un asistente experto en extraer información de extractos bancarios.

Analiza el siguiente texto de un extracto bancario y extrae TODAS las transacciones.

Para cada transacción, identifica:
- fecha: Fecha de la transacción (formato: YYYY-MM-DD)
- descripcion: Descripción o concepto de la transacción
- valor: Monto de la transacción (número positivo para ingresos, negativo para gastos)
- tipo: "ingreso" o "gasto"

IMPORTANTE:
- Devuelve SOLO un JSON válido, sin texto adicional
- El JSON debe ser un array de objetos
- Si no encuentras transacciones, devuelve un array vacío []

Texto del extracto:
{text}

Responde únicamente con el JSON:
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en análisis de extractos bancarios. Respondes SOLO con JSON válido."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            raw_output = response.choices[0].message.content
            transacciones = json.loads(raw_output)
            
            if isinstance(transacciones, dict) and "transacciones" in transacciones:
                transacciones = transacciones["transacciones"]
            
            return transacciones
        
        except json.JSONDecodeError as e:
            raise Exception(f"Error al parsear JSON: {str(e)}\nRespuesta: {raw_output}")
        
        except Exception as e:
            raise Exception(f"Error en la API de OpenAI: {str(e)}")
    
    
    def process_pdf(self, pdf_path: str) -> List[Dict]:
        """
        Procesa un PDF completo y extrae las transacciones
        
        Args:
            pdf_path: Ruta del archivo PDF
            
        Returns:
            Lista de transacciones extraídas
        """
        print(f" Leyendo PDF: {pdf_path}")
        text = self.extract_text_from_pdf(pdf_path)
        
        print(f"Texto extraído ({len(text)} caracteres)")
        print(f" Enviando a OpenAI para análisis...")
        
        transacciones = self.extract_transactions_from_text(text)
        
        print(f" {len(transacciones)} transacciones encontradas")
        
        return transacciones
    
    
    def save_to_csv(self, transacciones: List[Dict], output_path: str = "transacciones.csv"):
        """
        Guarda las transacciones en un archivo CSV
        
        Args:
            transacciones: Lista de transacciones
            output_path: Ruta del archivo CSV de salida
        """
        if not transacciones:
            print(" No hay transacciones para guardar")
            return
        
        fieldnames = set()
        for t in transacciones:
            fieldnames.update(t.keys())
        
        fieldnames = sorted(fieldnames)
        
        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transacciones)
        
        print(f" Archivo CSV generado: {output_path}")
    
    
    def save_to_json(self, transacciones: List[Dict], output_path: str = "transacciones.json"):
        """
        Guarda las transacciones en un archivo JSON
        
        Args:
            transacciones: Lista de transacciones
            output_path: Ruta del archivo JSON de salida
        """
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(transacciones, f, ensure_ascii=False, indent=2)
        
        print(f" Archivo JSON generado: {output_path}")


if __name__ == "__main__":
    
    API_KEY = os.getenv("OPENAI_API_KEY")
    
    extractor = OpenAIBankExtractor(api_key=API_KEY)
    
    pdf_path = "../ExtractoPrueba.pdf"
    
    try:
        transacciones = extractor.process_pdf(pdf_path)
        
        print("\n" + "="*60)
        print("TRANSACCIONES EXTRAÍDAS:")
        print("="*60)
        for i, t in enumerate(transacciones, 1):
            print(f"\n{i}. {t}")
        
        extractor.save_to_csv(transacciones, "transacciones.csv")
        extractor.save_to_json(transacciones, "transacciones.json")
        
        print("\n Proceso completado exitosamente!")
    
    except Exception as e:
        print(f"\n Error: {str(e)}")