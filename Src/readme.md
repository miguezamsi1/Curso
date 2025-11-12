# Plataforma de registro y recuperación de usuarios

Aplicación web en **Flask** que permite registrar usuarios institucionales y restablecer la contraseña mediante el envío de un correo electrónico. La interfaz se diseñó con una paleta en tonos celestes, blancos y detalles amarillos.

## Requisitos previos

1. **Python 3.11+**
2. **PostgreSQL 14+** con una base de datos llamada `usuarios`.
3. Credenciales SMTP del correo institucional desde el que se enviarán los mensajes.
4. [Poetry](https://python-poetry.org/) o `pip` para instalar dependencias.

## Preparación del entorno

1. Crea y activa un entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows usa .venv\\Scripts\\activate
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Copia el archivo de variables de entorno y ajústalo:
   ```bash
   cp .env.example .env
   ```
   Edita los valores de `.env` con las credenciales reales de la base de datos PostgreSQL y del servidor de correo.

## Configuración de la base de datos existente

La aplicación trabaja con la tabla `usuarios`. Si ya existe, asegúrate de que cuente con las columnas necesarias. En `database/alter_usuarios.sql` se incluye un script SQL para agregar los campos utilizados por la aplicación:

```sql
\i database/alter_usuarios.sql
```

> **Nota:** los campos `contrasena_hash`, `reset_token` y `reset_token_expira` se emplean para gestionar las contraseñas y los enlaces de recuperación.

## Migraciones (opcional)

Si prefieres manejar los cambios mediante migraciones de Flask-Migrate:

```bash
flask --app manage.py db init      # sólo la primera vez
flask --app manage.py db migrate -m "ajustes usuarios"
flask --app manage.py db upgrade
```

## Ejecución en modo desarrollo

1. Exporta la variable `FLASK_APP` si no usas el flag `--app`:
   ```bash
   export FLASK_APP=manage.py
   ```
2. Inicia la aplicación:
   ```bash
   flask --app manage.py run
   ```

Visita `http://127.0.0.1:5000` para acceder a la plataforma. Desde allí podrás:

- Registrar nuevos usuarios.
- Solicitar el restablecimiento de contraseña (envío de correo con token).
- Definir una nueva contraseña a partir del enlace recibido.

## Estructura principal del proyecto

```
app/
├── __init__.py
├── config.py
├── models.py
├── routes.py
├── static/
│   └── css/styles.css
└── templates/
    ├── base.html
    ├── index.html
    ├── registro.html
    ├── olvide_contrasena.html
    ├── restablecer_contrasena.html
    └── correo_recuperacion.html
```

## Envío de correos de recuperación

La función `enviar_correo` usa `Flask-Mail`. Verifica que las credenciales configuradas en `.env` permitan el envío SMTP (en Gmail se recomienda usar contraseñas de aplicación).

## Pruebas manuales sugeridas

1. Registrar un nuevo usuario desde `/registro`.
2. Solicitar recuperación de contraseña con ese mismo correo.
3. Abrir el enlace recibido y actualizar la contraseña.

Si no cuentas con un servidor SMTP, puedes usar el modo de depuración de Flask-Mail exportando `MAIL_SUPPRESS_SEND=true` para registrar los correos en consola mientras realizas las pruebas.
