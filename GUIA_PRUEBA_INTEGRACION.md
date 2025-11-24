# Guía Rápida de Prueba - Integración de Consultas

## 🚀 Inicio Rápido

### 1. Iniciar el Servidor de Desarrollo

```powershell
cd C:\Sistemas\eea
python manage.py runserver
```

### 2. Acceder al Sistema

Abrir navegador en: **http://localhost:8000/auth/login/**

---

## 📋 Pasos para Probar la Integración

### PASO 1: Login de Usuario
1. **URL:** http://localhost:8000/auth/login/
2. **Ingresar:**
   - Cédula de un usuario registrado
   - Contraseña del usuario
3. **Click en:** "Iniciar Sesión"

### PASO 2: Visualización Automática de Planillas
- **El sistema automáticamente:**
  - Toma la cédula del usuario desde la sesión
  - Consulta el servicio web SOAP de SAP
  - Muestra TODOS los servicios eléctricos del usuario
  - **NO requiere llenar ningún formulario adicional**

### PASO 3: Explorar la Información Mostrada

#### A. Información del Cliente (Sección Superior)
Verá una tarjeta celeste con:
- ✅ Nombres y apellidos
- ✅ Cédula/RUC
- ✅ Email
- ✅ Teléfono
- ✅ Celular
- ✅ Total de servicios

#### B. Listado de Servicios (Cards Blancas)
Cada servicio muestra:
- **Cuenta de Contrato** (número grande en azul)
- **Badge de Deuda:**
  - 🔴 Rojo si tiene deuda → Muestra el monto
  - 🟢 Verde si está al día → "Sin deuda"
- **Dirección** del servicio
- **Número de medidor**
- **Número de cuenta**
- **Meses adeudados**
- **Estado del contrato** (Activo/Inactivo)

### PASO 4: Ver Documentos y Facturas
1. En cualquier servicio, hacer click en:  
   **"Ver Documentos y Facturas"** (botón celeste)
2. Se abre un modal
3. Seleccionar año del dropdown:
   - Año actual (2024)
   - Año anterior (2023)
   - Hace 2 años (2022)
4. El sistema carga automáticamente las facturas de ese año
5. Se muestra tabla con:
   - Número de documento
   - Fecha de emisión
   - Número de factura
   - Fecha de vencimiento
   - Tipo de documento
   - Valor

---

## 🎨 Características Visuales Implementadas

### Diseño Corporativo
- **Colores:** Azul institucional (#003D82), Celeste (#40A9E3), Blanco
- **Animaciones:** Hover effects en las tarjetas de servicios
- **Iconos:** Font Awesome 6.4.0 para mejor UX
- **Responsivo:** Se adapta a móviles, tablets y desktop

### Indicadores Visuales
- **Badge Rojo:** Servicio con deuda pendiente
- **Badge Verde:** Servicio sin deuda (al día)
- **Badge "Activo":** Contrato activo (verde)
- **Badge "Inactivo":** Contrato suspendido (rojo)

---

## ✅ Checklist de Verificación

### Funcionalidad Básica
- [ ] Login exitoso redirige a `/auth/consultas/`
- [ ] Aparece nombre del usuario en el header
- [ ] Se muestra información del cliente (nombres, cédula, email, etc.)
- [ ] Se listan todos los servicios eléctricos del usuario

### Datos de Servicios
- [ ] Cada servicio muestra cuenta de contrato (VKONT)
- [ ] Se visualiza correctamente el monto de deuda
- [ ] Aparece la dirección del servicio
- [ ] Se muestra el número de medidor
- [ ] Badge de estado es visible (Activo/Inactivo)
- [ ] Meses adeudados aparecen correctamente

### Funcionalidad de Documentos
- [ ] Click en "Ver Documentos" abre modal
- [ ] Selector de año está visible
- [ ] Al seleccionar año, aparece spinner de carga
- [ ] Se muestra tabla con documentos (si existen)
- [ ] Mensaje de "No se encontraron documentos" si no hay datos
- [ ] Valores monetarios se muestran con símbolo de dólar

### Seguridad
- [ ] No se puede acceder a `/auth/consultas/` sin login
- [ ] Solo se muestran servicios del usuario autenticado
- [ ] Botón "Cerrar Sesión" funciona correctamente
- [ ] Después de cerrar sesión, redirige a verificar usuario

### Auditoría (Base de Datos)
Ejecutar en Python shell:
```python
from appeea.models import EventoSeguridad
EventoSeguridad.objects.filter(tipo_evento='CONSULTA_PLANILLA').order_by('-fecha_evento')[:5]
```
- [ ] Se registran eventos de consulta exitosa
- [ ] Se registran errores si el servicio falla

---

## 🐛 Posibles Problemas y Soluciones

### Problema 1: No se muestran los servicios
**Diagnóstico:**
```python
# En Django shell
python manage.py shell
>>> from appeea.servicios_consultas import obtener_servicio
>>> datos = obtener_servicio('CEDRUC', '0102030405', '', '')
>>> print(datos)
```

**Soluciones:**
- Verificar conexión al servidor SAP
- Verificar credenciales del servicio SOAP
- Revisar que la cédula existe en el sistema SAP

### Problema 2: Error "NoneType object has no attribute 'text'"
**Causa:** El servicio SOAP no retorna datos para esa cédula

**Solución:** 
- Usar una cédula que tenga servicios registrados en SAP
- Verificar que la cédula esté escrita correctamente

### Problema 3: No se cargan los documentos
**Verificar:**
1. Que la URL `/documentos/` está configurada en `urls.py`
2. Que la función `documentos()` en `views.py` funciona
3. Revisar la consola del navegador (F12) para errores JavaScript

**Solución:**
```python
# Verificar endpoint manualmente
import requests
from django.test import Client
client = Client()
response = client.post('/documentos/', {'ctacontrato': '123456', 'anio': '2024'})
print(response.content)
```

### Problema 4: Estilos no se cargan
**Solución:**
```powershell
python manage.py collectstatic --noinput
```
Luego refrescar el navegador con Ctrl + Shift + R

---

## 📊 Datos de Prueba Recomendados

### Usuario de Prueba
Si aún no tienes un usuario registrado, crear uno:

1. Ir a http://localhost:8000/auth/verificar/
2. Ingresar cédula que exista en el sistema SAP
3. Completar proceso de registro
4. Ingresar código dactilar de prueba

### Cédulas con Servicios Registrados
Usar cédulas que sepas que tienen servicios eléctricos activos en el sistema de la EEA.

---

## 📸 Capturas Esperadas

### Pantalla 1: Login
- Formulario con campos de cédula y contraseña
- Botón "Iniciar Sesión"
- Enlaces a recuperar contraseña y registro

### Pantalla 2: Consulta de Planillas (Después del Login)
- **Header:** "Mis Planillas" con ícono de factura
- **Subtítulo:** "Bienvenido/a [Nombre del Usuario]"
- **Tarjeta Celeste:** Información del cliente (6 campos)
- **Título:** "Mis Servicios Eléctricos"
- **Cards Blancas:** Una por cada servicio
  - Número de cuenta grande en azul
  - Badge de deuda a la derecha (rojo o verde)
  - Grid con información del servicio
  - Botón celeste "Ver Documentos y Facturas"

### Pantalla 3: Modal de Documentos
- **Header azul:** "Documentos y Facturas"
- **Selector de año:** Dropdown con 3 años
- **Tabla:** Headers en celeste claro, filas blancas alternadas
- **Columnas:** Documento, Fecha Doc., Núm. Factura, Fecha Venc., Tipo, Valor

---

## 🎯 Flujo de Éxito Completo

1. ✅ Usuario abre http://localhost:8000/auth/login/
2. ✅ Ingresa cédula: `0102030405` y contraseña
3. ✅ Click en "Iniciar Sesión"
4. ✅ Redirige automáticamente a `/auth/consultas/`
5. ✅ Aparece mensaje: "Bienvenido/a Juan Pérez"
6. ✅ Se muestra tarjeta celeste con datos del cliente
7. ✅ Aparecen 2 servicios en cards blancas
   - Servicio 1: Cuenta 100012345, Deuda $45.80 (rojo), Dirección "Calle Principal 123"
   - Servicio 2: Cuenta 100067890, Sin deuda (verde), Dirección "Av. Central 456"
8. ✅ Click en "Ver Documentos" del servicio 1
9. ✅ Modal se abre con selector de año
10. ✅ Selecciona "2024"
11. ✅ Aparece tabla con 8 facturas del año 2024
12. ✅ Cierra modal
13. ✅ Click en "Actualizar Información" → página recarga
14. ✅ Click en "Cerrar Sesión" → redirige a login

---

## 📝 Notas Importantes

### Diferencia con el Sistema Antiguo

**Sistema Antiguo** (`/consulta-planillas/`):
- Usuario debe ingresar cédula en formulario
- No requiere autenticación
- Cualquiera puede consultar cualquier cédula
- Interfaz desactualizada

**Sistema Nuevo** (`/auth/consultas/`):
- Requiere login primero
- Cédula se obtiene automáticamente de la sesión
- Solo puede ver su propia información
- Interfaz moderna con diseño corporativo
- Registro de auditoría

### Convivencia de Ambos Sistemas

Ambos sistemas pueden coexistir:
- **Antiguo:** `/consulta-planillas/` (público, requiere cédula manual)
- **Nuevo:** `/auth/consultas/` (protegido, automático)

Se recomienda mantener el antiguo para usuarios no registrados y el nuevo para usuarios con cuenta.

---

## 🔐 Auditoría y Seguridad

### Revisar Eventos de Seguridad

Acceder al admin de Django:
1. http://localhost:8000/admin/
2. Login con superusuario
3. Ir a "Eventos de Seguridad"
4. Filtrar por tipo: "CONSULTA_PLANILLA"
5. Ver detalles:
   - Usuario que consultó
   - Fecha y hora
   - Dirección IP
   - Descripción del evento

### Consulta SQL Directa
```sql
SELECT 
    u.nombres || ' ' || u.apellidos as usuario,
    e.tipo_evento,
    e.descripcion,
    e.ip_address,
    e.fecha_evento
FROM appeea_eventoseguridad e
JOIN appeea_usuarioregistrado u ON e.usuario_id = u.id_usuario
WHERE e.tipo_evento IN ('CONSULTA_PLANILLA', 'ERROR_CONSULTA')
ORDER BY e.fecha_evento DESC
LIMIT 20;
```

---

## 📞 Soporte

Si encuentra algún problema durante las pruebas:

1. **Revisar logs de Django** en la consola donde corre el servidor
2. **Revisar consola del navegador** (F12) para errores JavaScript
3. **Verificar base de datos** con Django Admin
4. **Consultar documentación** en `INTEGRACION_SERVICIO_CONSULTAS.md`

---

**¡Listo para probar!** 🎉

La integración está completa y lista para pruebas. El flujo es completamente automático:  
**Login → Ver Planillas Inmediatamente**

No se requiere ningún formulario adicional ni ingresar la cédula nuevamente.
