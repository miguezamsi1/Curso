# Sistema Web Institucional EEA

Página web institucional desarrollada en Django para la Empresa Eléctrica Azogues (EEA).

## 📌 Información del Proyecto

- **Versión actual:** 1.0.0
- **Última actualización:** Noviembre 2025
- **Framework:** Django
- **Base de datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Repositorio:** https://github.com/miguezamsi1/Curso

## 📋 Requisitos Previos

- Python 3.13 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para control de versiones)

## 🚀 Instalación Rápida

### Opción 1: Usando scripts automatizados (Recomendado)

**Para Desarrollo:**
```powershell
.\iniciar_desarrollo.ps1
```
o
```cmd
iniciar_desarrollo.bat
```

**Para Producción:**
```powershell
.\iniciar_produccion.ps1
```
o
```cmd
iniciar_produccion.bat
```

### Opción 2: Instalación manual

1. **Crear y activar entorno virtual:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. **Instalar dependencias:**
```powershell
pip install -r requirements_prod.txt
```

3. **Aplicar migraciones:**
```powershell
python manage.py migrate
```

4. **Crear superusuario:**
```powershell
python manage.py createsuperuser
```
Sigue las instrucciones para crear el usuario administrador.

5. **Recopilar archivos estáticos:**
```powershell
python manage.py collectstatic
```

6. **Iniciar servidor:**

**Desarrollo:**
```powershell
python manage.py runserver 0.0.0.0:8000
```

**Producción (Windows):**
```powershell
pip install waitress
waitress-serve --port=8000 eea.wsgi:application
```

## 🌐 Acceso al Sistema

Una vez iniciado el servidor, podrás acceder a:

- **Sitio web público:** http://localhost:8000/
- **Panel de administración:** http://localhost:8000/admin/

## 📁 Estructura del Proyecto

```
eea/
├── appeea/              # Aplicación principal
│   ├── migrations/      # Migraciones de base de datos
│   ├── templates/       # Plantillas HTML
│   ├── models.py        # Modelos de base de datos
│   ├── views.py         # Vistas de la aplicación
│   └── urls.py          # URLs de la aplicación
├── eea/                 # Configuración del proyecto
│   ├── settings.py      # Configuración general
│   ├── urls.py          # URLs principales
│   └── wsgi.py          # Punto de entrada WSGI
├── media/               # Archivos subidos por usuarios
├── static/              # Archivos estáticos (CSS, JS, imágenes)
├── staticfiles/         # Archivos estáticos recopilados
├── venv/                # Entorno virtual
├── db.sqlite3           # Base de datos SQLite
└── manage.py            # Script de administración Django
```

## 🔧 Configuración

### Variables de Entorno

Copia el archivo `.env.example` a `.env` y ajusta los valores según tu entorno:

```
DEBUG=False
SECRET_KEY=tu-clave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1,www.eea.gob.ec,eea.gob.ec
```

### Base de Datos

Por defecto, el sistema usa SQLite (`db.sqlite3`). Para usar PostgreSQL o MySQL en producción:

1. Instala el driver correspondiente:
```powershell
# PostgreSQL
pip install psycopg2

# MySQL
pip install mysqlclient
```

2. Modifica `DATABASES` en `eea/settings.py`:

**PostgreSQL:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_base_datos',
        'USER': 'usuario',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**MySQL:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nombre_base_datos',
        'USER': 'usuario',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## 📝 Funcionalidades del Sistema

- **Gestión de Noticias:** Publicación y administración de noticias institucionales
- **Transparencia:** Sección para documentos de transparencia organizados por año y mes
- **Servicios:** Información sobre servicios institucionales
- **Institución:** Información institucional
- **Procesos de Contratación:** Gestión multinivel de procesos
- **Rendición de Cuentas:** Documentos de rendición organizados por año y fase
- **Enlaces de Interés:** Gestión de enlaces externos
- **Editor WYSIWYG:** Utilizando CKEditor para contenido rico
- **Geolocalización:** Integración con Google Maps
- **Imágenes optimizadas:** Recorte y redimensionamiento automático

## 🔐 Seguridad

Para producción, asegúrate de:

1. ✅ Cambiar `SECRET_KEY` en `settings.py` por una clave única y segura
2. ✅ Establecer `DEBUG = False`
3. ✅ Configurar `ALLOWED_HOSTS` con los dominios permitidos
4. ✅ Usar HTTPS en producción
5. ✅ Configurar una base de datos robusta (PostgreSQL/MySQL)
6. ✅ Configurar backups regulares de la base de datos
7. ✅ Mantener las dependencias actualizadas

## 🐛 Solución de Problemas

### Error: "No module named 'django'"
```powershell
# Asegúrate de que el entorno virtual esté activado
.\venv\Scripts\Activate.ps1
pip install Django==4.2.17
```

### Error al ejecutar migraciones
```powershell
# Eliminar la base de datos y volver a crearla
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Archivos estáticos no se cargan
```powershell
# Recopilar archivos estáticos nuevamente
python manage.py collectstatic --clear --noinput
```

## 📦 Dependencias Principales

- Django 4.2.17 - Framework web
- django-ckeditor 6.7.3 - Editor WYSIWYG
- django-import-export 4.3.14 - Importar/Exportar datos
- django-image-cropping 1.7 - Recorte de imágenes
- django-geoposition-2 0.4.0 - Campos de geolocalización
- Pillow 12.0.0 - Procesamiento de imágenes
- whitenoise 6.11.0 - Servir archivos estáticos
- waitress 23.0.0 - Servidor WSGI para Windows

## 🔄 Actualización del Sistema

```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Actualizar dependencias
pip install -r requirements_prod.txt --upgrade

# Aplicar nuevas migraciones
python manage.py migrate

# Recopilar archivos estáticos
python manage.py collectstatic --noinput
```

## 📞 Soporte

Para problemas o consultas sobre el sistema, contactar al administrador del sistema.

## 📄 Licencia

Este sistema es propiedad de la Empresa Eléctrica Ambato (EEA).

---

**Última actualización:** Noviembre 2025
**Versión Django:** 4.2.17
**Python:** 3.13+
