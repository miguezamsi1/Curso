# 🎉 Instalación Completada - Pasos Finales

## ✅ Lo que se ha configurado

1. ✅ Entorno virtual Python creado en `venv/`
2. ✅ Todas las dependencias instaladas y actualizadas a versiones compatibles
3. ✅ Base de datos SQLite creada y migraciones aplicadas
4. ✅ Archivos estáticos recopilados en `staticfiles/`
5. ✅ Configuración de producción con WhiteNoise
6. ✅ Scripts de inicio creados (PowerShell y Batch)

## 🚀 Pasos Finales para Iniciar el Sistema

### Paso 1: Crear el Superusuario (OBLIGATORIO)

Ejecuta el siguiente comando para crear el usuario administrador:

```powershell
.\venv\Scripts\Activate.ps1
python manage.py createsuperuser
```

Te pedirá:
- **Username:** admin (o el que prefieras)
- **Email:** admin@eea.gob.ec
- **Password:** (mínimo 8 caracteres)
- **Password (again):** (confirmar)

### Paso 2: Iniciar el Servidor

**Para Desarrollo (con auto-reload):**
```powershell
.\iniciar_desarrollo.ps1
```

**Para Producción:**
```powershell
.\iniciar_produccion.ps1
```

### Paso 3: Acceder al Sistema

Una vez iniciado el servidor:

- **Sitio Web:** http://localhost:8000/
- **Panel Admin:** http://localhost:8000/admin/

Usa las credenciales del superusuario que creaste.

## 📝 Configuración Inicial en el Panel de Administración

1. **Accede al panel:** http://localhost:8000/admin/
2. **Configura IndexGeneral:**
   - Sube el logo de la institución
   - Configura enlaces a redes sociales
   - Configura el mapa y ubicación
   - Personaliza el pie de página

3. **Crea contenido inicial:**
   - Noticias
   - Servicios
   - Información institucional
   - Enlaces de interés

## 🌐 Despliegue en Producción

### Opción 1: Servidor Windows con IIS

1. Instala IIS con soporte para FastCGI
2. Instala `wfastcgi`:
   ```powershell
   pip install wfastcgi
   wfastcgi-enable
   ```
3. Configura IIS para apuntar a `eea.wsgi:application`

### Opción 2: Servidor Linux con Nginx + Gunicorn

1. Instala Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Crea un servicio systemd:
   ```bash
   sudo nano /etc/systemd/system/eea.service
   ```

3. Contenido del servicio:
   ```ini
   [Unit]
   Description=EEA Django Application
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/ruta/a/eea
   Environment="PATH=/ruta/a/eea/venv/bin"
   ExecStart=/ruta/a/eea/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 eea.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

4. Configura Nginx como proxy inverso

### Opción 3: Usar Waitress (Recomendado para Windows)

Ya está incluido en el script `iniciar_produccion.ps1`

## 🔒 Checklist de Seguridad para Producción

Antes de poner en producción, verifica:

- [ ] Cambiar `SECRET_KEY` en `settings.py` por una clave única
- [ ] Establecer `DEBUG = False` en `settings.py`
- [ ] Configurar `ALLOWED_HOSTS` con tu dominio real
- [ ] Cambiar contraseña del superusuario a algo seguro
- [ ] Configurar HTTPS/SSL
- [ ] Configurar backup automático de `db.sqlite3` (o migrar a PostgreSQL)
- [ ] Configurar firewall para permitir solo puerto 80/443
- [ ] Actualizar la API Key de Google Maps si es necesaria

## 📊 Migración a PostgreSQL (Recomendado para Producción)

1. Instala PostgreSQL y crea una base de datos

2. Instala el driver:
   ```powershell
   pip install psycopg2
   ```

3. Modifica `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'eea_db',
           'USER': 'eea_user',
           'PASSWORD': 'tu_contraseña_segura',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

4. Exporta datos de SQLite e importa a PostgreSQL:
   ```powershell
   python manage.py dumpdata > backup.json
   # Cambia la configuración de base de datos
   python manage.py migrate
   python manage.py loaddata backup.json
   ```

## 🔄 Mantenimiento Regular

### Backup de Base de Datos
```powershell
# Exportar datos
python manage.py dumpdata --natural-foreign --natural-primary > backup_$(Get-Date -Format "yyyyMMdd_HHmmss").json

# Backup de archivos media
Copy-Item -Path media -Destination "backup_media_$(Get-Date -Format 'yyyyMMdd')" -Recurse
```

### Actualización del Sistema
```powershell
# Actualizar dependencias
pip install -r requirements_prod.txt --upgrade

# Aplicar migraciones
python manage.py migrate

# Recopilar estáticos
python manage.py collectstatic --noinput
```

## 📞 Información de Contacto

Para soporte técnico o consultas sobre el sistema, contactar al administrador del sistema.

## 📚 Recursos Adicionales

- [Documentación de Django](https://docs.djangoproject.com/)
- [Documentación de CKEditor](https://ckeditor.com/docs/)
- [Guía de Despliegue Django](https://docs.djangoproject.com/en/4.2/howto/deployment/)

---

**¡El sistema está listo para usar!** 🎉

Ejecuta `.\iniciar_desarrollo.ps1` para comenzar.
