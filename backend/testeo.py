import asyncio
import asyncpg

async def test_connection(user, password, host, port, database):
    try:
        print(f"Probando conexión con usuario: {user}")
        conn = await asyncpg.connect(
            user=user,
            password=password,
            database=database,
            host=host,
            port=port,
            timeout=10
        )
        print("✅ ¡Conexión exitosa!")
        version = await conn.fetchval('SELECT version()')
        print(f"PostgreSQL version: {version}")
        await conn.close()
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    password = "qaKEbEi6t8uhTq7V"
    host = "aws-1-sa-east-1.pooler.supabase.com"
    port = 5432
    database = "postgres"
    
    # Probar diferentes formatos de usuario
    usuarios = [
        "postgres.xdnvzetsoduzoxwxnzd",
        "postgres",
        "xdnvzetsoduzoxwxnzd",
    ]
    
    for user in usuarios:
        print(f"\n{'='*50}")
        success = await test_connection(user, password, host, port, database)
        if success:
            print(f"\n🎉 Usuario correcto: {user}")
            break
    
    # Probar también el puerto 6543 (Transaction mode)
    print(f"\n{'='*50}")
    print("Probando puerto 6543 (Transaction mode)...")
    await test_connection("postgres.xdnvzetsoduzoxwxnzd", password, host, 6543, database)

asyncio.run(main())