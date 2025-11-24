# 🚀 Guía Rápida de Prueba - Módulo de Autenticación EEA

## ✅ Pasos para Probar el Sistema

### 1. Iniciar el Servidor de Desarrollo

```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Iniciar servidor
python manage.py runserver
```

### 2. Acceder al Módulo

Abrir en el navegador: **http://localhost:8000/auth/verificar/**

### 3. Flujo de Prueba Completo

#### A. Registro de Nuevo Usuario

1. **Verificación Inicial**
   - URL: `/auth/verificar/`
   - Ingresar: `0123456789` (cédula de prueba)
   - Click en "Verificar Registro"

2. **Proceso CHECKING**
   - Leer términos LOPDP
   - Marcar checkbox de aceptación
   - Click en "Continuar con el Registro"

3. **Registro de Usuario**
   - Nombres: `JUAN CARLOS`
   - Apellidos: `PÉREZ LÓPEZ`
   - Email: `tu-email@gmail.com` (usar un email real para recibir códigos)
   - Contraseña: `123456` (o la que prefieras, mínimo 6 caracteres)
   - Confirmar contraseña
   - Click en "Crear Cuenta"

4. **Confirmación de Correo**
   - Click en "Enviar Código de Verificación"
   - Revisar email (y carpeta de spam)
   - Ingresar código de 6 dígitos
   - Click en "Verificar Código"

5. **Validación de Identidad**
   - Ingresar código dactilar de prueba: `AB123456CD`
   - Click en "Completar Registro"

6. **Login Exitoso**
   - Cédula: `0123456789`
   - Contraseña: la que configuraste
   - Click en "Ingresar"

7. **Consulta de Planillas**
   - Acceso automático al área protegida
   - Ver información del usuario
   - Opciones de consulta disponibles

#### B. Recuperación de Contraseña

1. Ir a `/auth/login/`
2. Click en "Recuperar Contraseña"
3. Ingresar email registrado
4. Revisar código en email
5. Ingresar código y nueva contraseña
6. Login con nueva contraseña

### 4. Verificar en el Panel de Administración

```
URL: http://localhost:8000/admin/
Usuario: tu superusuario de Django
```

Ver:
- **Usuarios Registrados**: Lista de usuarios creados
- **Códigos de Verificación**: Códigos enviados
- **Eventos de Seguridad**: Log de accesos y eventos

## 🎨 Elementos de UI/UX a Verificar

### Diseño Visual
- ✅ Colores corporativos (azul #003D82, celeste #40A9E3, blanco)
- ✅ Sombras suaves en cards
- ✅ Bordes redondeados (10px-16px)
- ✅ Iconos Font Awesome
- ✅ Animaciones de entrada (fadeIn, slideUp)

### Funcionalidades
- ✅ Auto-mayúsculas en nombres y apellidos
- ✅ Icono de ojo para mostrar/ocultar contraseñas
- ✅ Validación de campos en tiempo real
- ✅ Mensajes de error/éxito con iconos
- ✅ Responsive design (probar en móvil)

## 📧 Configuración de Email (Importante)

El sistema está configurado para usar SMTP. **Para pruebas reales**:

1. Editar `eea/settings.py`:

```python
EMAIL_HOST = 'smtp.gmail.com'  # O tu servidor SMTP
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu-contraseña-app'  # Contraseña de aplicación
```

2. Si usas Gmail, crear una "Contraseña de aplicación":
   - Ir a: https://myaccount.google.com/apppasswords
   - Generar contraseña para "Correo"
   - Usar esa contraseña en settings.py

**Alternativa para pruebas sin email:**
- Los códigos también se imprimen en la consola del servidor
- Buscar en el terminal: `Código de verificación: XXXXXX`

## 🔍 Casos de Prueba

### Caso 1: Usuario Nuevo
- ✅ Verificar cédula no registrada
- ✅ Aceptar términos
- ✅ Completar registro
- ✅ Verificar email
- ✅ Validar identidad
- ✅ Login exitoso

### Caso 2: Usuario Existente
- ✅ Verificar cédula registrada
- ✅ Redirección a login
- ✅ Login con credenciales

### Caso 3: Recuperación de Contraseña
- ✅ Solicitar código
- ✅ Recibir email
- ✅ Cambiar contraseña
- ✅ Login con nueva contraseña

### Caso 4: Validaciones
- ❌ Contraseñas no coinciden
- ❌ Código incorrecto
- ❌ Código expirado (15 min)
- ❌ Email duplicado
- ❌ Cédula duplicada

## 📊 Base de Datos

### Tablas Creadas
- `usuario_registrado`
- `codigo_verificacion`
- `evento_seguridad`

### Consultar Usuarios
```python
python manage.py shell

from appeea.models import UsuarioRegistrado
usuarios = UsuarioRegistrado.objects.all()
for u in usuarios:
    print(f"{u.cedula} - {u.nombres} {u.apellidos} - {u.email}")
```

### Ver Eventos de Seguridad
```python
from appeea.models import EventoSeguridad
eventos = EventoSeguridad.objects.all().order_by('-fecha_evento')
for e in eventos:
    print(f"{e.tipo_evento} - {e.descripcion} - {e.fecha_evento}")
```

## 🐛 Solución de Problemas

### Email no llega
- Verificar configuración SMTP en settings.py
- Revisar carpeta de spam
- Ver código en consola del servidor

### Error de migraciones
```powershell
python manage.py makemigrations
python manage.py migrate
```

### CSS no carga
```powershell
python manage.py collectstatic
```

### Error 404 en /auth/
- Verificar que `appeea/urls.py` está actualizado
- Reiniciar el servidor

## ✨ Características Destacadas

1. **Seguridad**
   - Contraseñas hasheadas
   - Códigos de un solo uso
   - Expiración de códigos (15 min)
   - Registro de eventos con IP

2. **UX/UI**
   - Diseño corporativo profesional
   - Animaciones suaves
   - Responsive
   - Mensajes claros

3. **Funcionalidad**
   - Flujo completo de registro
   - Verificación por email
   - Recuperación de contraseña
   - Sistema de sesiones
   - Área protegida

## 📞 Próximos Pasos

1. Integrar con módulo de consulta de planillas existente
2. Agregar más validaciones de cédula ecuatoriana
3. Implementar 2FA (autenticación de dos factores)
4. Dashboard completo de usuario
5. Notificaciones personalizadas

---

**¡Sistema listo para usar!** 🎉

Para más información, consultar `MODULO_AUTENTICACION.md`
