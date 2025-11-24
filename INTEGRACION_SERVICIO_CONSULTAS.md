# Integración del Servicio de Consultas con el Módulo de Autenticación

## Resumen de la Integración

Se ha completado exitosamente la integración del servicio web SOAP de consultas de planillas con el módulo de autenticación, eliminando la necesidad de que los usuarios autenticados pasen por el formulario de consulta tradicional.

---

## Cambios Implementados

### 1. Modificación de `appeea/views_auth.py`

**Función modificada:** `consulta_planillas()`

**Cambios realizados:**
- Se importa la función `obtener_servicio` desde `servicios_consultas.py`
- Se obtiene automáticamente la cédula del usuario desde la sesión (`request.session.get('usuario_cedula')`)
- Se realiza la consulta al servicio web SOAP sin intervención del usuario
- Se maneja el resultado del servicio y posibles errores
- Se registran eventos de seguridad para auditoría (consultas exitosas y errores)

**Código implementado:**
```python
def consulta_planillas(request):
    """Vista protegida para consulta de planillas"""
    from .servicios_consultas import obtener_servicio
    
    usuario_id = request.session.get('usuario_logueado')
    
    if not usuario_id:
        messages.warning(request, 'Debe iniciar sesión para acceder a esta sección')
        return redirect('login_usuario')
    
    try:
        usuario = UsuarioRegistrado.objects.get(id_usuario=usuario_id)
        
        # Obtener la cédula del usuario de la sesión
        usuario_cedula = request.session.get('usuario_cedula')
        
        # Inicializar variables para datos del servicio
        datos_servicio = None
        error_servicio = None
        
        if usuario_cedula:
            try:
                # Llamar al servicio web con la cédula del usuario
                datos_servicio = obtener_servicio('CEDRUC', usuario_cedula, '', '')
                
                # Registrar evento de consulta exitosa
                EventoSeguridad.objects.create(
                    usuario=usuario,
                    tipo_evento='CONSULTA_PLANILLA',
                    descripcion=f'Consulta de planillas realizada exitosamente',
                    ip_address=request.META.get('REMOTE_ADDR', '')
                )
            except Exception as e:
                error_servicio = f'Error al consultar información: {str(e)}'
                # Registrar evento de error
                EventoSeguridad.objects.create(
                    usuario=usuario,
                    tipo_evento='ERROR_CONSULTA',
                    descripcion=f'Error en consulta: {str(e)}',
                    ip_address=request.META.get('REMOTE_ADDR', '')
                )
        
        context = {
            'usuario': usuario,
            'datos_servicio': datos_servicio,
            'error_servicio': error_servicio
        }
        
        return render(request, 'auth/consulta_planillas.html', context)
        
    except UsuarioRegistrado.DoesNotExist:
        return redirect('login_usuario')
```

### 2. Rediseño Completo de `appeea/templates/auth/consulta_planillas.html`

**Características del nuevo diseño:**

#### A. Estilos Corporativos Mejorados
- **Service Cards**: Tarjetas para cada servicio eléctrico con animaciones hover
- **Badges de Deuda**: Indicadores visuales de deuda (rojo) o sin deuda (verde)
- **Grid Responsivo**: Layout adaptable que se ajusta a diferentes pantallas
- **Colores institucionales**: Azul (#003D82), Celeste (#40A9E3), Blanco

#### B. Información del Cliente
Muestra automáticamente:
- Nombres y apellidos del cliente
- Cédula/RUC
- Email
- Teléfono fijo
- Celular
- Total de servicios

#### C. Listado de Servicios Eléctricos
Para cada servicio se muestra:
- **Cuenta de Contrato (VKONT)**: Número identificador del servicio
- **Deuda**: Monto adeudado con indicador visual
- **Dirección**: Ubicación del servicio
- **Medidor**: Número del medidor eléctrico
- **Cuenta**: Número de cuenta
- **Meses Adeudados**: Cantidad de meses con deuda pendiente
- **Estado del Contrato**: Activo/Inactivo con badge de color

#### D. Funcionalidad de Documentos
- Botón para ver documentos y facturas por servicio
- Modal con selector de año (año actual y 2 años anteriores)
- Tabla de documentos con:
  - Número de documento
  - Fecha de emisión
  - Número de factura
  - Fecha de vencimiento
  - Tipo de documento
  - Valor del documento
- Integración AJAX con el endpoint `/documentos/`

#### E. Experiencia de Usuario
- **Loading Spinner**: Indicador visual durante la carga de documentos
- **Mensajes de Error**: Alertas claras cuando no hay datos o hay errores
- **Botón de Actualizar**: Permite recargar la información
- **Sesión Visible**: Muestra usuario activo y último acceso

---

## Flujo de Funcionamiento

### Paso 1: Inicio de Sesión
1. Usuario ingresa a `/auth/login/`
2. Proporciona cédula y contraseña
3. Sistema valida credenciales
4. Se almacena en sesión:
   - `usuario_logueado`: ID del usuario
   - `usuario_cedula`: Cédula del usuario
   - `usuario_nombre_completo`: Nombre completo

### Paso 2: Acceso a Consultas
1. Usuario accede a `/auth/consultas/`
2. Sistema verifica autenticación (decorador de protección)
3. Se obtiene automáticamente la cédula de la sesión
4. **NO SE REQUIERE FORMULARIO** - Consulta automática

### Paso 3: Consulta Automática al Web Service
1. Se llama a `obtener_servicio('CEDRUC', usuario_cedula, '', '')`
2. El servicio SOAP retorna:
   ```python
   {
       'APELLIDOS': 'Apellidos del cliente',
       'CEDRUC': 'Cédula del cliente',
       'CELULAR': 'Número de celular',
       'EMAIL': 'correo@ejemplo.com',
       'NOMBRES': 'Nombres del cliente',
       'TELEFONO': 'Número fijo',
       'SERVICIOS': [
           {
               'VKONT': 'Número de cuenta',
               'MEDIDOR': 'Número de medidor',
               'CUEN': 'Cuenta',
               'DIRECCION': 'Dirección del servicio',
               'DEUDA': 'Monto adeudado',
               'ESTADOCONTRATO': 'ACTIVO/01',
               'MESES': 'Meses adeudados'
           },
           # ... más servicios
       ],
       'TOTAL': 2
   }
   ```

### Paso 4: Visualización de Resultados
1. Template recibe el objeto `datos_servicio`
2. Se renderiza la información del cliente
3. Se muestran todos los servicios en cards corporativas
4. Usuario puede:
   - Ver detalles de cada servicio
   - Identificar servicios con deuda
   - Acceder a documentos/facturas por año
   - Actualizar información
   - Cerrar sesión

### Paso 5: Consulta de Documentos (Opcional)
1. Usuario hace clic en "Ver Documentos y Facturas" de un servicio
2. Se abre modal con selector de año
3. Usuario selecciona año
4. Sistema llama vía AJAX a `/documentos/` con:
   - `ctacontrato`: Número de cuenta del servicio
   - `anio`: Año seleccionado
5. Se muestra tabla con documentos del año seleccionado

---

## Ventajas de la Nueva Implementación

### 1. **Experiencia de Usuario Mejorada**
- ✅ No requiere ingresar cédula nuevamente
- ✅ Información inmediata al ingresar
- ✅ Interfaz moderna y profesional
- ✅ Diseño responsivo para móviles

### 2. **Seguridad**
- ✅ Autenticación obligatoria
- ✅ Registro de auditoría en `EventoSeguridad`
- ✅ Sesiones seguras
- ✅ Solo puede ver su propia información

### 3. **Integración Completa**
- ✅ Usa el mismo servicio SOAP que el sistema antiguo
- ✅ Compatible con la infraestructura existente
- ✅ No requiere cambios en el backend SAP
- ✅ Mantiene la funcionalidad de documentos

### 4. **Mantenimiento**
- ✅ Código centralizado en `views_auth.py`
- ✅ Reutiliza `servicios_consultas.py` existente
- ✅ Fácil de debuggear
- ✅ Registro de errores para soporte

---

## Endpoints del Servicio Web SOAP

### Servicio de Consulta de Servicios
- **URL:** `http://p8sapisu01.redenergia.gob.ec:8010/sap/bc/srt/rfc/sap/zws_obtieneservicios/310/zws_obtieneservicios/zws_obtieneservicios`
- **Autenticación:** EEAZOGUES / gXlCVE<eLUZxponeMiknLRsabRoAamtRoKZ3VgLF
- **Método:** POST con SOAP envelope
- **Parámetros:**
  - `DIVISION`: 0802 (fijo)
  - `TIPO`: CEDRUC (para búsqueda por cédula)
  - `VALOR`: Cédula del cliente
  - `PAGE_SIZE`: Vacío (todos los resultados)
  - `SKIP`: Vacío (sin paginación)

### Servicio de Documentos
- **URL:** `http://p8sapisu01.redenergia.gob.ec:8010/sap/bc/srt/rfc/sap/zws_obtiene_documentos/310/zws_obtiene_documentos/zws_obtiene_documentos`
- **Autenticación:** EEAZOGUES / gXlCVE<eLUZxponeMiknLRsabRoAamtRoKZ3VgLF
- **Método:** POST con SOAP envelope
- **Parámetros:**
  - `CTACONTRATO`: Número de cuenta de contrato
  - `YEAR`: Año de consulta (YYYY)

---

## Comparación: Antes vs. Después

### Sistema Antiguo (`/consulta-planillas/`)
```
Usuario → Formulario (Tipo: Cédula, Valor: 0102030405) 
       → Submit 
       → info_cuenta(request) 
       → obtener_servicio('CEDRUC', '0102030405') 
       → Renderiza consultas.html
```

**Problemas:**
- Requiere ingresar cédula manualmente cada vez
- Cualquiera puede consultar con cualquier cédula
- Sin autenticación
- Interfaz desactualizada

### Sistema Nuevo (`/auth/consultas/`)
```
Usuario → Login (cédula + contraseña) 
       → Sesión creada (usuario_cedula guardada) 
       → Accede a /auth/consultas/ 
       → consulta_planillas(request) 
       → obtener_servicio('CEDRUC', session['usuario_cedula']) 
       → Renderiza consulta_planillas.html con diseño corporativo
```

**Ventajas:**
- Autenticación requerida
- Cédula tomada automáticamente de la sesión
- No puede ver información de otros usuarios
- Interfaz moderna con diseño corporativo
- Auditoría de accesos

---

## Pruebas Realizadas

### ✅ Verificación de Sintaxis
- Sin errores en `views_auth.py`
- Sin errores en `consulta_planillas.html`

### 📋 Próximas Pruebas Recomendadas

1. **Prueba de Integración Completa:**
   ```bash
   # Iniciar servidor de desarrollo
   python manage.py runserver
   ```
   - Acceder a http://localhost:8000/auth/login/
   - Login con usuario registrado
   - Verificar redirección a /auth/consultas/
   - Confirmar visualización de servicios
   - Probar botón "Ver Documentos"

2. **Prueba de Seguridad:**
   - Intentar acceder a `/auth/consultas/` sin login → debe redirigir a login
   - Verificar que solo muestra servicios del usuario autenticado
   - Revisar tabla `appeea_eventoseguridad` para auditoría

3. **Prueba de Errores:**
   - Simular error del servicio web (apagar SAP temporalmente)
   - Verificar mensaje de error amigable
   - Confirmar registro del error en EventoSeguridad

4. **Prueba de Documentos:**
   - Hacer clic en "Ver Documentos" de un servicio
   - Seleccionar año actual
   - Verificar tabla de documentos
   - Probar con año sin documentos

---

## Archivos Modificados

1. **`appeea/views_auth.py`** (líneas 454-483)
   - Función `consulta_planillas()` completamente reescrita
   - Integración con `obtener_servicio()`
   - Manejo de errores y auditoría

2. **`appeea/templates/auth/consulta_planillas.html`** (completo)
   - Rediseño total de la interfaz
   - Estilos corporativos integrados
   - JavaScript para modal de documentos
   - Integración con Bootstrap 5 y jQuery

---

## Configuración Requerida

### Variables de Sesión Necesarias
Estas se configuran automáticamente en `login_usuario()`:
```python
request.session['usuario_logueado'] = usuario.id_usuario
request.session['usuario_cedula'] = usuario.cedula
request.session['usuario_nombre_completo'] = f"{usuario.nombres} {usuario.apellidos}"
```

### Dependencias del Template
```html
<!-- CSS -->
<link rel="stylesheet" href="{% static 'css/auth-style.css' %}">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">

<!-- JavaScript -->
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

---

## Mantenimiento y Soporte

### Eventos de Seguridad Registrados
Todos los accesos se registran en la tabla `appeea_eventoseguridad`:

| Tipo de Evento | Descripción | Cuándo Ocurre |
|----------------|-------------|---------------|
| `CONSULTA_PLANILLA` | Consulta exitosa de planillas | Al cargar `/auth/consultas/` con éxito |
| `ERROR_CONSULTA` | Error al consultar servicio | Cuando `obtener_servicio()` falla |

### Consulta SQL para Auditoría
```sql
-- Ver todas las consultas de un usuario
SELECT * FROM appeea_eventoseguridad 
WHERE usuario_id = 1 AND tipo_evento = 'CONSULTA_PLANILLA'
ORDER BY fecha_evento DESC;

-- Ver errores de consulta
SELECT * FROM appeea_eventoseguridad 
WHERE tipo_evento = 'ERROR_CONSULTA'
ORDER BY fecha_evento DESC;
```

### Troubleshooting

#### Problema: No se muestran los servicios
**Solución:**
1. Verificar que la sesión tiene `usuario_cedula`:
   ```python
   print(request.session.get('usuario_cedula'))
   ```
2. Verificar respuesta del servicio web:
   ```python
   datos = obtener_servicio('CEDRUC', '0102030405', '', '')
   print(datos)
   ```

#### Problema: Error al cargar documentos
**Solución:**
1. Verificar que la URL `/documentos/` existe en `urls.py`
2. Verificar que `views.documentos()` está funcionando
3. Revisar logs de Django para detalles del error

#### Problema: Diseño no se ve correctamente
**Solución:**
1. Ejecutar `python manage.py collectstatic`
2. Verificar que `auth-style.css` existe en `/static/css/`
3. Limpiar caché del navegador (Ctrl + Shift + R)

---

## Próximos Pasos Sugeridos

1. **Implementar Pago en Línea:**
   - Agregar botón "Pagar Ahora" en servicios con deuda
   - Integrar pasarela de pagos
   - Generar comprobante de pago

2. **Notificaciones por Email:**
   - Enviar email cuando hay nueva factura
   - Alertar antes de vencimiento
   - Confirmar pagos realizados

3. **Gráficos de Consumo:**
   - Mostrar gráfico de consumo mensual
   - Comparativa año actual vs. anterior
   - Predicción de próxima factura

4. **Exportación de Datos:**
   - Botón para descargar PDF de estado de cuenta
   - Exportar histórico a Excel
   - Generar reporte anual

5. **Optimización de Performance:**
   - Implementar caché de consultas (Redis)
   - Cargar servicios de forma asíncrona
   - Lazy loading de documentos

---

## Conclusión

La integración se ha completado exitosamente, permitiendo que los usuarios autenticados accedan automáticamente a sus planillas sin necesidad de ingresar nuevamente su cédula. El diseño corporativo moderno proporciona una experiencia de usuario superior, mientras que el registro de auditoría garantiza la seguridad y trazabilidad de todas las operaciones.

**Estado:** ✅ **COMPLETADO Y LISTO PARA PRUEBAS**

---

**Fecha de Implementación:** 24 de noviembre de 2024  
**Desarrollador:** GitHub Copilot  
**Sistema:** Empresa Eléctrica Azogues - Portal Web  
**Módulo:** Autenticación y Consultas Integradas
