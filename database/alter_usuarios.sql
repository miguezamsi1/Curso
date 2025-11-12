-- Ajustes sugeridos para la tabla existente "usuarios"
-- Ejecutar en la base de datos PostgreSQL "usuarios"

ALTER TABLE usuarios
    ADD COLUMN IF NOT EXISTS nombre VARCHAR(120) NOT NULL DEFAULT 'Usuario',
    ADD COLUMN IF NOT EXISTS correo VARCHAR(120) UNIQUE NOT NULL,
    ADD COLUMN IF NOT EXISTS contrasena_hash VARCHAR(255) NOT NULL DEFAULT '',
    ADD COLUMN IF NOT EXISTS reset_token VARCHAR(255),
    ADD COLUMN IF NOT EXISTS reset_token_expira TIMESTAMP,
    ADD COLUMN IF NOT EXISTS creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Elimina el valor por defecto temporal y asegura que los campos sean obligatorios una vez actualizados
ALTER TABLE usuarios ALTER COLUMN nombre DROP DEFAULT;
ALTER TABLE usuarios ALTER COLUMN contrasena_hash DROP DEFAULT;
