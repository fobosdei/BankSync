-- Migration: Fix users table schema to match UserModels
-- Date: 2025-01-XX
-- Description: Agrega campos faltantes (password_hash, last_login) y corrige metadata

-- 1. Agregar password_hash (necesario para autenticación)
ALTER TABLE public.users 
ADD COLUMN IF NOT EXISTS password_hash text;

-- 2. Agregar last_login (para tracking de sesiones)
ALTER TABLE public.users 
ADD COLUMN IF NOT EXISTS last_login timestamp with time zone;

-- 3. Crear columna 'metadata' si no existe (para almacenar datos adicionales en JSONB)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = 'users' 
        AND column_name = 'metadata'
    ) THEN
        ALTER TABLE public.users 
        ADD COLUMN metadata jsonb DEFAULT '{}'::jsonb;
    END IF;
END $$;

-- 4. Asegurar que el default de 'role' sea 'viewer' (como en el schema original)
ALTER TABLE public.users 
ALTER COLUMN role SET DEFAULT 'viewer';

-- 5. Hacer password_hash NOT NULL después de migrar datos existentes
-- (Comentar esta línea si hay usuarios sin password_hash)
-- ALTER TABLE public.users ALTER COLUMN password_hash SET NOT NULL;

-- 6. Crear índice en email si no existe (ya debería existir por UNIQUE, pero por si acaso)
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);

-- Verificación: Ver estructura final
-- SELECT column_name, data_type, is_nullable, column_default
-- FROM information_schema.columns
-- WHERE table_schema = 'public' AND table_name = 'users'
-- ORDER BY ordinal_position;
