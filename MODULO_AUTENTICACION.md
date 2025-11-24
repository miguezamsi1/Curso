# Módulo de Registro y Verificación de Usuarios - EEA

## 📋 Descripción

Sistema completo de autenticación, registro y verificación de usuarios con diseño UI/UX corporativo profesional para la Empresa Eléctrica Azogues.

## 🎨 Características de Diseño

### Paleta de Colores Corporativa
- **Azul Institucional**: #003D82
- **Celeste**: #40A9E3
- **Blanco**: #FFFFFF

### Estilo Visual
- ✅ Diseño ejecutivo, moderno y elegante
- ✅ Minimalista, ordenado y limpio
- ✅ Elementos con sombras suaves
- ✅ Bordes redondeados
- ✅ Iconos estilizados (Font Awesome 6.4.0)
- ✅ Tipografía moderna y corporativa
- ✅ Animaciones suaves y fluidas

## 🔐 Funcionalidades Implementadas

### Pantalla 1: Verificación Inicial
- Consulta si el usuario está registrado en la base de datos
- Redirección automática según el estado
- Información LOPDP visible

### Pantalla 2: Proceso CHECKING
- Aceptación de términos y condiciones
- Explicación clara de la LOPDP
- Validación de consentimiento

### Pantalla 3: Registro de Usuario
- Formulario completo con validación
- Auto-mayúsculas en nombres y apellidos
- Validación de contraseñas
- Campos obligatorios claramente indicados

### Pantalla 4: Confirmación de Correo
- Envío de código de 6 dígitos por SMTP
- Validación de código con expiración (15 minutos)
- Opción de reenvío de código
- Registro de eventos de seguridad

### Pantalla 5: Validación de Identidad
- Solicitud de código dactilar
- Diseño serio y sobrio
- Mensajes de seguridad claros

### Pantalla 6: Login de Usuario
- Acceso con cédula y contraseña
- Visualización de contraseña con icono de ojo
- Opción "Olvidé mi contraseña"
- Registro de intentos de login

### Pantalla 7: Recuperación de Credenciales
- Solicitud por email
- Código de verificación
- Cambio seguro de contraseña
- Registro de eventos en BD

### Área Protegida: Consulta de Planillas
- Acceso solo para usuarios autenticados
- Dashboard con información del usuario
- Opciones de consulta
- Panel de servicios disponibles

## 📊 Modelos de Base de Datos

### UsuarioRegistrado
```python
- cedula (único)
- nombres
- apellidos
- email (único)
- password (hasheada)
- codigo_dactilar
- verificado (Boolean)
- activo (Boolean)
- fecha_registro
- ultimo_acceso
```

### CodigoVerificacion
```python
- usuario (FK)
- codigo (6 dígitos)
- tipo (email/recuperacion)
- usado (Boolean)
- fecha_creacion
- fecha_expiracion
```

### EventoSeguridad
```python
- usuario (FK)
- tipo_evento
- descripcion
- ip_address
- fecha_evento
```

## 📧 Configuración de Email SMTP

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'webmaster@eea.com.ec'
EMAIL_HOST_PASSWORD = 'TestEnvMail.77'
```

## 🚀 URLs Disponibles

```python
/auth/verificar/                  # Verificación inicial
/auth/checking/                   # Proceso CHECKING
/auth/registro/                   # Registro de usuario
/auth/confirmacion-correo/        # Verificación de email
/auth/validacion-identidad/       # Código dactilar
/auth/login/                      # Login
/auth/recuperacion/               # Recuperar contraseña
/auth/verificar-recuperacion/     # Cambiar contraseña
/auth/logout/                     # Cerrar sesión
/auth/consultas/                  # Consulta de planillas (protegida)
```

## 🛡️ Seguridad Implementada

- ✅ Contraseñas hasheadas con `make_password`
- ✅ Códigos de verificación con expiración
- ✅ Registro de eventos de seguridad
- ✅ Validación de sesiones
- ✅ Protección de rutas con autenticación
- ✅ Registro de IP en eventos críticos
- ✅ Códigos de un solo uso

## 📱 Responsive Design

- Adaptable a dispositivos móviles
- Diseño fluid y flexible
- Experiencia optimizada para tablets y smartphones

## 🎯 Próximos Pasos

1. Integrar con el módulo existente de consulta de planillas
2. Agregar autenticación de dos factores (2FA)
3. Implementar recuperación por SMS
4. Dashboard completo de usuario
5. Historial de accesos
6. Notificaciones por email

## 📝 Uso Básico

### Para Usuario Final

1. Ingresar en `/auth/verificar/`
2. Introducir número de cédula
3. Si no está registrado, completar el proceso de registro
4. Verificar email con código
5. Ingresar código dactilar
6. Iniciar sesión
7. Acceder a consulta de planillas

### Para Administrador

- Acceder al panel de administración Django
- Gestionar usuarios en "Usuarios Registrados"
- Ver códigos de verificación
- Auditar eventos de seguridad

## 🔧 Mantenimiento

### Ver eventos de seguridad
```python
from appeea.models import EventoSeguridad
eventos = EventoSeguridad.objects.all().order_by('-fecha_evento')
```

### Limpiar códigos expirados
```python
from appeea.models import CodigoVerificacion
from django.utils import timezone
CodigoVerificacion.objects.filter(fecha_expiracion__lt=timezone.now()).delete()
```

## 📞 Soporte

Para soporte técnico o consultas sobre el módulo, contactar al equipo de desarrollo de EEA.

---

**Desarrollado con Django | Diseño UI/UX Corporativo EEA**
**Versión 1.0.0 | Noviembre 2025**
