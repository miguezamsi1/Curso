# 🚀 Guía de Implementación en Servidor de Producción

## 📋 Pre-requisitos

Antes de implementar en el servidor de EEA, verificar:

- ✅ Servidor tiene acceso a la red interna de EEA
- ✅ Servidor puede resolver DNS: `p8sapisu01.redenergia.gob.ec`
- ✅ Puerto 8010 accesible desde el servidor
- ✅ Python 3.x instalado
- ✅ Git instalado

---

## 📦 Pasos de Implementación

### 1. Conectarse al Servidor

```bash
# SSH o Escritorio Remoto al servidor de EEA
ssh usuario@servidor-eea
# O usar Remote Desktop
```

### 2. Clonar o Actualizar Repositorio

#### Si es primera vez:
```bash
cd /ruta/donde/instalar
git clone https://github.com/miguezamsi1/Curso.git eea
cd eea
```

#### Si ya existe:
```bash
cd /ruta/eea
git pull origin main
```

### 3. Crear Entorno Virtual

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows Server
python -m venv venv
venv\Scripts\activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar Base de Datos

```bash
python manage.py migrate
```

### 6. Crear Superusuario (si no existe)

```bash
python manage.py createsuperuser
```

### 7. Colectar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

### 8. Verificar Conectividad a SAP

```bash
# Desde el servidor, verificar:
ping p8sapisu01.redenergia.gob.ec

# Verificar puerto 8010
telnet p8sapisu01.redenergia.gob.ec 8010
# o en PowerShell:
Test-NetConnection -ComputerName p8sapisu01.redenergia.gob.ec -Port 8010
```

**Resultado esperado:**
```
TcpTestSucceeded : True
```

---

## ⚙️ Configuración del Servidor Web

### Opción 1: Apache con mod_wsgi

#### Instalar mod_wsgi
```bash
pip install mod_wsgi
```

#### Configuración Apache
```apache
<VirtualHost *:80>
    ServerName eea.gob.ec
    ServerAlias www.eea.gob.ec
    
    WSGIDaemonProcess eea python-home=/ruta/eea/venv python-path=/ruta/eea
    WSGIProcessGroup eea
    WSGIScriptAlias / /ruta/eea/eea/wsgi.py
    
    <Directory /ruta/eea/eea>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    
    Alias /static /ruta/eea/staticfiles
    <Directory /ruta/eea/staticfiles>
        Require all granted
    </Directory>
    
    Alias /media /ruta/eea/media
    <Directory /ruta/eea/media>
        Require all granted
    </Directory>
</VirtualHost>
```

#### Reiniciar Apache
```bash
sudo systemctl restart apache2
# o
sudo service apache2 restart
```

### Opción 2: Nginx + Gunicorn

#### Instalar Gunicorn
```bash
pip install gunicorn
```

#### Crear servicio systemd
```bash
sudo nano /etc/systemd/system/eea.service
```

Contenido:
```ini
[Unit]
Description=EEA Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/ruta/eea
Environment="PATH=/ruta/eea/venv/bin"
ExecStart=/ruta/eea/venv/bin/gunicorn --workers 3 --bind unix:/ruta/eea/eea.sock eea.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### Configuración Nginx
```nginx
server {
    listen 80;
    server_name eea.gob.ec www.eea.gob.ec;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /ruta/eea/staticfiles/;
    }
    
    location /media/ {
        alias /ruta/eea/media/;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/ruta/eea/eea.sock;
    }
}
```

#### Iniciar servicios
```bash
sudo systemctl start eea
sudo systemctl enable eea
sudo systemctl restart nginx
```

### Opción 3: IIS (Windows Server)

#### 1. Instalar wfastcgi
```powershell
pip install wfastcgi
wfastcgi-enable
# Copiar la ruta que devuelve
```

#### 2. Crear web.config en la raíz del proyecto
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <handlers>
            <add name="Python FastCGI" 
                 path="*" 
                 verb="*" 
                 modules="FastCgiModule" 
                 scriptProcessor="C:\Sistemas\eea\venv\Scripts\python.exe|C:\Sistemas\eea\venv\Lib\site-packages\wfastcgi.py" 
                 resourceType="Unspecified" />
        </handlers>
    </system.webServer>
    <appSettings>
        <add key="WSGI_HANDLER" value="django.core.wsgi.get_wsgi_application()" />
        <add key="PYTHONPATH" value="C:\Sistemas\eea" />
        <add key="DJANGO_SETTINGS_MODULE" value="eea.settings" />
    </appSettings>
</configuration>
```

#### 3. Configurar IIS
1. Abrir IIS Manager
2. Agregar nuevo sitio web
3. Apuntar a la carpeta del proyecto
4. Configurar pool de aplicaciones para "Sin código administrado"

---

## 🔒 Configuración de Seguridad

### 1. Actualizar settings.py para Producción

```python
# eea/settings.py

# IMPORTANTE: Cambiar en producción
DEBUG = False

ALLOWED_HOSTS = ['eea.gob.ec', 'www.eea.gob.ec', 'IP_DEL_SERVIDOR']

# Configurar clave secreta única
SECRET_KEY = 'generar-una-clave-secreta-unica-y-segura'

# Configuración de base de datos de producción (si usa PostgreSQL/MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # o mysql
        'NAME': 'eea_db',
        'USER': 'eea_user',
        'PASSWORD': 'contraseña_segura',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 2. Generar SECRET_KEY Nueva

```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
# Copiar el resultado y pegarlo en settings.py
```

---

## ✅ Verificación Post-Implementación

### 1. Verificar que el sitio carga
```bash
curl http://localhost
# o
curl http://eea.gob.ec
```

### 2. Probar el módulo de autenticación

1. Acceder a: `http://eea.gob.ec/auth/login/`
2. Crear un usuario de prueba
3. Hacer login
4. Verificar que accede a `/auth/consultas/`
5. **Verificar que NO aparece banner naranja de "Modo Prueba"**
6. Verificar que se muestran datos REALES del SAP

### 3. Probar consulta de planillas

1. Login con usuario
2. Debe ver automáticamente sus servicios eléctricos
3. Click en "Ver Documentos y Facturas"
4. Seleccionar año
5. Verificar que se cargan documentos reales

### 4. Verificar auditoría

```bash
python manage.py shell
>>> from appeea.models import EventoSeguridad
>>> EventoSeguridad.objects.filter(tipo_evento='CONSULTA_PLANILLA').latest('fecha_evento')
# Debe mostrar la consulta sin "(MODO PRUEBA)"
```

### 5. Verificar logs de error

```bash
# Linux
tail -f /var/log/apache2/error.log
# o
tail -f /var/log/nginx/error.log

# Windows Server
# Ver Visor de Eventos de Windows
```

---

## 🐛 Troubleshooting en Producción

### Error: No se muestran los estilos CSS

**Solución:**
```bash
python manage.py collectstatic --noinput
sudo systemctl restart apache2  # o nginx
```

### Error: "Bad Request (400)"

**Causa:** `ALLOWED_HOSTS` no configurado

**Solución:**
```python
# settings.py
ALLOWED_HOSTS = ['eea.gob.ec', 'www.eea.gob.ec', 'IP_DEL_SERVIDOR']
```

### Error: No se conecta al servidor SAP

**Verificar:**
```bash
# Desde el servidor
ping p8sapisu01.redenergia.gob.ec
telnet p8sapisu01.redenergia.gob.ec 8010
```

**Revisar firewall:**
```bash
# Permitir tráfico saliente al puerto 8010
sudo ufw allow out 8010
```

### Error: Permission denied

**Solución:**
```bash
# Dar permisos correctos
sudo chown -R www-data:www-data /ruta/eea
sudo chmod -R 755 /ruta/eea
```

---

## 📊 Monitoreo

### Logs de Django

Configurar en `settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/eea-error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Monitorear consultas a SAP

```sql
-- Consultas exitosas en las últimas 24 horas
SELECT COUNT(*) 
FROM appeea_eventoseguridad 
WHERE tipo_evento = 'CONSULTA_PLANILLA' 
  AND fecha_evento >= datetime('now', '-1 day');

-- Errores en las últimas 24 horas
SELECT COUNT(*) 
FROM appeea_eventoseguridad 
WHERE tipo_evento = 'ERROR_CONSULTA' 
  AND fecha_evento >= datetime('now', '-1 day');
```

---

## 🔄 Actualizaciones Futuras

Cuando haya cambios en el código:

```bash
# 1. Conectar al servidor
ssh usuario@servidor-eea

# 2. Ir a la carpeta del proyecto
cd /ruta/eea

# 3. Hacer backup de la base de datos
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d)

# 4. Actualizar código
git pull origin main

# 5. Activar entorno virtual
source venv/bin/activate  # Linux
# o
venv\Scripts\activate  # Windows

# 6. Instalar nuevas dependencias (si hay)
pip install -r requirements.txt

# 7. Aplicar migraciones
python manage.py migrate

# 8. Colectar estáticos
python manage.py collectstatic --noinput

# 9. Reiniciar servidor web
sudo systemctl restart apache2  # o nginx o gunicorn
```

---

## 📞 Checklist Final

Antes de dar por finalizada la implementación:

- [ ] Servidor web corriendo (Apache/Nginx/IIS)
- [ ] Sitio accesible desde navegador
- [ ] `DEBUG = False` en settings.py
- [ ] `SECRET_KEY` única generada
- [ ] `ALLOWED_HOSTS` configurado correctamente
- [ ] Archivos estáticos cargando (CSS, JS, imágenes)
- [ ] Login funciona correctamente
- [ ] Consulta de planillas muestra datos REALES de SAP
- [ ] NO aparece banner naranja "Modo Prueba"
- [ ] Modal de documentos funciona
- [ ] Se registran eventos en EventoSeguridad
- [ ] Servidor SAP accesible (ping y puerto 8010)
- [ ] HTTPS configurado (certificado SSL)
- [ ] Backups configurados
- [ ] Logs configurados
- [ ] Usuarios de prueba validados

---

## 📝 Información Importante

### Credenciales SAP
```
Servidor: p8sapisu01.redenergia.gob.ec:8010
Usuario: EEAZOGUES
Contraseña: gXlCVE<eLUZxponeMiknLRsabRoAamtRoKZ3VgLF
```

### URLs del Sistema
- **Login:** http://eea.gob.ec/auth/login/
- **Consultas:** http://eea.gob.ec/auth/consultas/
- **Admin:** http://eea.gob.ec/admin/

### Contacto Soporte
- **Desarrollo:** [Tu contacto]
- **IT EEA:** [Contacto del departamento de IT]

---

**Fecha de implementación:** _______________  
**Implementado por:** _______________  
**Servidor:** _______________  
**IP:** _______________

---

✅ **Sistema listo para producción**  
🚀 **Sin modo de prueba - Solo datos reales de SAP**
