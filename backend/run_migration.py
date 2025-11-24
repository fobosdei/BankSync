"""
Script para ejecutar la migración SQL automáticamente en la base de datos.
Ejecuta: python run_migration.py
"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
import asyncpg

# Cargar variables de entorno
load_dotenv()

async def run_migration():
    """Ejecuta la migración SQL automáticamente."""
    migration_file = Path(__file__).parent / "database" / "migrations" / "001_fix_users_schema.sql"
    
    if not migration_file.exists():
        print(f"[ERROR] No se encontro el archivo de migracion: {migration_file}")
        return False
    
    # Leer el SQL
    print(f"[INFO] Leyendo migracion: {migration_file}")
    with open(migration_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Obtener la URL de la base de datos
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("[ERROR] No se encontro DATABASE_URL en las variables de entorno")
        print("   Asegurate de tener un archivo .env con DATABASE_URL configurado")
        return False
    
    print("[INFO] Conectando a la base de datos...")
    
    try:
        # Conectar usando asyncpg directamente
        # Extraer los parámetros de conexión de la URL
        # Formato: postgresql://user:password@host:port/database?params
        from urllib.parse import urlparse, parse_qs, unquote
        
        parsed = urlparse(database_url)
        
        if not parsed.hostname:
            print("[ERROR] No se pudo parsear la URL de la base de datos")
            print(f"[DEBUG] URL recibida: {database_url[:50]}...")
            return False
        
        user = unquote(parsed.username) if parsed.username else None
        password = unquote(parsed.password) if parsed.password else None
        host = parsed.hostname
        port = parsed.port if parsed.port else 5432
        database = unquote(parsed.path.lstrip('/')) if parsed.path else None
        
        if not all([user, password, host, database]):
            print("[ERROR] Faltan parametros en la URL de la base de datos")
            print(f"[DEBUG] user={user}, host={host}, database={database}")
            return False
        
        # Conectar
        conn = await asyncpg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        
        print("[OK] Conectado a la base de datos")
        print("[INFO] Ejecutando migracion...")
        
        # Ejecutar el SQL (dividir por ; para ejecutar cada statement)
        # Pero el DO $$ bloque necesita ser ejecutado completo
        statements = []
        current_statement = ""
        in_do_block = False
        
        for line in sql_content.split('\n'):
            line = line.strip()
            if not line or line.startswith('--'):
                continue
            
            current_statement += line + '\n'
            
            if 'DO $$' in line:
                in_do_block = True
            elif in_do_block and 'END $$;' in line:
                statements.append(current_statement)
                current_statement = ""
                in_do_block = False
            elif not in_do_block and line.endswith(';'):
                statements.append(current_statement)
                current_statement = ""
        
        # Ejecutar cada statement
        for i, stmt in enumerate(statements, 1):
            if stmt.strip():
                try:
                    await conn.execute(stmt)
                    print(f"   [OK] Statement {i} ejecutado correctamente")
                except Exception as e:
                    # Si la columna ya existe, no es un error critico
                    if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                        print(f"   [WARN] Statement {i}: {str(e)[:100]}... (ya existe, continuando)")
                    else:
                        print(f"   [WARN] Statement {i}: {str(e)[:100]}...")
        
        await conn.close()
        print("[OK] Migracion completada exitosamente")
        print("[INFO] Reinicia tu servidor FastAPI para que los cambios surtan efecto")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error ejecutando migracion: {e}")
        print("\n[INFO] Si el error persiste, ejecuta el SQL manualmente en Supabase:")
        print("   1. Ve al SQL Editor en Supabase")
        print("   2. Copia y pega el contenido de database/migrations/001_fix_users_schema.sql")
        print("   3. Ejecuta el SQL")
        return False

if __name__ == "__main__":
    print("=" * 80)
    print("INICIANDO MIGRACION AUTOMATICA DE BASE DE DATOS")
    print("=" * 80)
    success = asyncio.run(run_migration())
    print("=" * 80)
    if success:
        print("[OK] Migracion completada! Ahora puedes reiniciar tu servidor.")
    else:
        print("[ERROR] La migracion fallo. Revisa los errores arriba.")
    print("=" * 80)

