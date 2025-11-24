# -*- coding: utf-8 -*-
"""
Vistas para el Módulo de Registro y Verificación de Usuarios
Sistema de autenticación corporativo EEA
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
import random
import string

from .models import UsuarioRegistrado, CodigoVerificacion, EventoSeguridad


def get_client_ip(request):
    """Obtener IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generar_codigo_verificacion():
    """Genera un código aleatorio de 6 dígitos"""
    return ''.join(random.choices(string.digits, k=6))


def enviar_email_verificacion(email, codigo, nombres):
    """Envía email con código de verificación"""
    asunto = 'Código de Verificación - EEA'
    mensaje = f"""
    Estimado/a {nombres},
    
    Su código de verificación es: {codigo}
    
    Este código es válido por 15 minutos.
    
    Si usted no solicitó este código, por favor ignore este mensaje.
    
    Atentamente,
    Empresa Eléctrica Azogues
    """
    
    try:
        send_mail(
            asunto,
            mensaje,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error enviando email: {e}")
        return False


# Pantalla 1: Verificación Inicial de Usuario
def verificar_usuario(request):
    """Vista para verificar si el usuario está registrado"""
    if request.method == 'POST':
        cedula = request.POST.get('cedula', '').strip()
        
        if not cedula:
            messages.error(request, 'Por favor ingrese su número de cédula')
            return render(request, 'auth/verificar_usuario.html')
        
        # Verificar si existe el usuario
        try:
            usuario = UsuarioRegistrado.objects.get(cedula=cedula)
            # Usuario registrado, redirigir a login
            request.session['cedula_verificada'] = cedula
            return redirect('login_usuario')
        except UsuarioRegistrado.DoesNotExist:
            # Usuario NO registrado, mostrar aviso LOPDP
            request.session['cedula_nueva'] = cedula
            return redirect('proceso_checking')
    
    return render(request, 'auth/verificar_usuario.html')


# Pantalla 2: Proceso CHECKING
def proceso_checking(request):
    """Vista para aceptación de términos y condiciones LOPDP"""
    cedula = request.session.get('cedula_nueva')
    
    if not cedula:
        return redirect('verificar_usuario')
    
    if request.method == 'POST':
        aceptacion = request.POST.get('aceptacion_lopdp')
        
        if aceptacion == 'on':
            return redirect('registro_usuario')
        else:
            messages.warning(request, 'Debe aceptar los términos y condiciones para continuar')
    
    return render(request, 'auth/proceso_checking.html')


# Pantalla 3: Registro de Usuario Nuevo
def registro_usuario(request):
    """Vista para registro de nuevo usuario"""
    cedula = request.session.get('cedula_nueva')
    
    if not cedula:
        return redirect('verificar_usuario')
    
    if request.method == 'POST':
        nombres = request.POST.get('nombres', '').strip().upper()
        apellidos = request.POST.get('apellidos', '').strip().upper()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirmar_password = request.POST.get('confirmar_password', '')
        
        # Validaciones
        if not all([nombres, apellidos, email, password, confirmar_password]):
            messages.error(request, 'Todos los campos son obligatorios')
            return render(request, 'auth/registro_usuario.html', {'cedula': cedula})
        
        if password != confirmar_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'auth/registro_usuario.html', {'cedula': cedula})
        
        if len(password) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres')
            return render(request, 'auth/registro_usuario.html', {'cedula': cedula})
        
        # Verificar email único
        if UsuarioRegistrado.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return render(request, 'auth/registro_usuario.html', {'cedula': cedula})
        
        try:
            # Crear usuario
            usuario = UsuarioRegistrado.objects.create(
                cedula=cedula,
                nombres=nombres,
                apellidos=apellidos,
                email=email,
                password=make_password(password),
                verificado=False,
                activo=True
            )
            
            # Registrar evento
            EventoSeguridad.objects.create(
                usuario=usuario,
                tipo_evento='registro',
                descripcion=f'Nuevo registro de usuario: {cedula}',
                ip_address=get_client_ip(request)
            )
            
            # Guardar en sesión para siguiente paso
            request.session['usuario_id'] = usuario.id_usuario
            request.session['usuario_email'] = email
            request.session['usuario_nombres'] = nombres
            
            return redirect('confirmacion_correo')
            
        except Exception as e:
            messages.error(request, f'Error al registrar usuario: {str(e)}')
    
    return render(request, 'auth/registro_usuario.html', {'cedula': cedula})


# Pantalla 4: Confirmación de Correo
def confirmacion_correo(request):
    """Vista para envío y verificación de código por email"""
    usuario_id = request.session.get('usuario_id')
    
    if not usuario_id:
        return redirect('verificar_usuario')
    
    try:
        usuario = UsuarioRegistrado.objects.get(id_usuario=usuario_id)
    except UsuarioRegistrado.DoesNotExist:
        return redirect('verificar_usuario')
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        # Enviar código
        if accion == 'enviar':
            # Generar código
            codigo = generar_codigo_verificacion()
            
            # Guardar código en BD
            fecha_expiracion = timezone.now() + timedelta(minutes=15)
            CodigoVerificacion.objects.create(
                usuario=usuario,
                codigo=codigo,
                tipo='email',
                fecha_expiracion=fecha_expiracion
            )
            
            # Enviar email
            if enviar_email_verificacion(usuario.email, codigo, usuario.nombres):
                messages.success(request, f'Código enviado a {usuario.email}')
                request.session['codigo_enviado'] = True
            else:
                messages.error(request, 'Error al enviar el código. Intente nuevamente.')
        
        # Verificar código
        elif accion == 'verificar':
            codigo_ingresado = request.POST.get('codigo', '').strip()
            
            if not codigo_ingresado:
                messages.error(request, 'Por favor ingrese el código')
            else:
                # Buscar código válido
                try:
                    codigo_obj = CodigoVerificacion.objects.get(
                        usuario=usuario,
                        codigo=codigo_ingresado,
                        tipo='email',
                        usado=False,
                        fecha_expiracion__gt=timezone.now()
                    )
                    
                    # Marcar código como usado
                    codigo_obj.usado = True
                    codigo_obj.save()
                    
                    # Registrar evento
                    EventoSeguridad.objects.create(
                        usuario=usuario,
                        tipo_evento='verificacion_email',
                        descripcion='Email verificado correctamente',
                        ip_address=get_client_ip(request)
                    )
                    
                    messages.success(request, 'Email verificado correctamente')
                    return redirect('validacion_identidad')
                    
                except CodigoVerificacion.DoesNotExist:
                    messages.error(request, 'Código incorrecto o expirado')
    
    return render(request, 'auth/confirmacion_correo.html', {
        'usuario': usuario,
        'codigo_enviado': request.session.get('codigo_enviado', False)
    })


# Pantalla 5: Validación de Identidad Pública
def validacion_identidad(request):
    """Vista para validación con código dactilar"""
    usuario_id = request.session.get('usuario_id')
    
    if not usuario_id:
        return redirect('verificar_usuario')
    
    try:
        usuario = UsuarioRegistrado.objects.get(id_usuario=usuario_id)
    except UsuarioRegistrado.DoesNotExist:
        return redirect('verificar_usuario')
    
    if request.method == 'POST':
        codigo_dactilar = request.POST.get('codigo_dactilar', '').strip()
        
        if not codigo_dactilar:
            messages.error(request, 'Por favor ingrese su código dactilar')
        else:
            # Guardar código dactilar
            usuario.codigo_dactilar = codigo_dactilar
            usuario.verificado = True
            usuario.save()
            
            # Limpiar sesión
            request.session.pop('cedula_nueva', None)
            request.session.pop('usuario_id', None)
            request.session.pop('usuario_email', None)
            request.session.pop('codigo_enviado', None)
            
            messages.success(request, 'Registro completado exitosamente. Ya puede iniciar sesión.')
            return redirect('login_usuario')
    
    return render(request, 'auth/validacion_identidad.html', {'usuario': usuario})


# Pantalla 6: Login Usuario Existente
def login_usuario(request):
    """Vista para login de usuario registrado"""
    if request.method == 'POST':
        cedula = request.POST.get('cedula', '').strip()
        password = request.POST.get('password', '')
        
        if not cedula or not password:
            messages.error(request, 'Por favor ingrese su cédula y contraseña')
            return render(request, 'auth/login_usuario.html')
        
        try:
            usuario = UsuarioRegistrado.objects.get(cedula=cedula, activo=True)
            
            # Verificar contraseña
            if check_password(password, usuario.password):
                # Login exitoso
                usuario.ultimo_acceso = timezone.now()
                usuario.save()
                
                # Registrar evento
                EventoSeguridad.objects.create(
                    usuario=usuario,
                    tipo_evento='login_exitoso',
                    descripcion='Login exitoso',
                    ip_address=get_client_ip(request)
                )
                
                # Guardar en sesión
                request.session['usuario_logueado'] = usuario.id_usuario
                request.session['usuario_cedula'] = usuario.cedula
                request.session['usuario_nombre_completo'] = f'{usuario.nombres} {usuario.apellidos}'
                
                messages.success(request, f'Bienvenido/a {usuario.nombres}')
                return redirect('consulta_planillas')
            else:
                # Contraseña incorrecta
                EventoSeguridad.objects.create(
                    usuario=usuario,
                    tipo_evento='login_fallido',
                    descripcion='Contraseña incorrecta',
                    ip_address=get_client_ip(request)
                )
                messages.error(request, 'Contraseña incorrecta')
        
        except UsuarioRegistrado.DoesNotExist:
            messages.error(request, 'Usuario no encontrado o inactivo')
    
    return render(request, 'auth/login_usuario.html')


# Pantalla 7: Recuperación de Credenciales
def recuperacion_credenciales(request):
    """Vista para recuperación de contraseña"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        
        if not email:
            messages.error(request, 'Por favor ingrese su email')
            return render(request, 'auth/recuperacion_credenciales.html')
        
        try:
            usuario = UsuarioRegistrado.objects.get(email=email, activo=True)
            
            # Generar código
            codigo = generar_codigo_verificacion()
            fecha_expiracion = timezone.now() + timedelta(minutes=15)
            
            CodigoVerificacion.objects.create(
                usuario=usuario,
                codigo=codigo,
                tipo='recuperacion',
                fecha_expiracion=fecha_expiracion
            )
            
            # Enviar email
            if enviar_email_verificacion(email, codigo, usuario.nombres):
                # Registrar evento
                EventoSeguridad.objects.create(
                    usuario=usuario,
                    tipo_evento='recuperacion_password',
                    descripcion='Solicitud de recuperación de contraseña',
                    ip_address=get_client_ip(request)
                )
                
                request.session['recuperacion_usuario_id'] = usuario.id_usuario
                messages.success(request, f'Se ha enviado un código de verificación a {email}')
                return redirect('verificar_codigo_recuperacion')
            else:
                messages.error(request, 'Error al enviar el código. Intente nuevamente.')
        
        except UsuarioRegistrado.DoesNotExist:
            messages.error(request, 'Email no encontrado en nuestros registros')
    
    return render(request, 'auth/recuperacion_credenciales.html')


def verificar_codigo_recuperacion(request):
    """Vista para verificar código y cambiar contraseña"""
    usuario_id = request.session.get('recuperacion_usuario_id')
    
    if not usuario_id:
        return redirect('recuperacion_credenciales')
    
    try:
        usuario = UsuarioRegistrado.objects.get(id_usuario=usuario_id)
    except UsuarioRegistrado.DoesNotExist:
        return redirect('recuperacion_credenciales')
    
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        nueva_password = request.POST.get('nueva_password', '')
        confirmar_password = request.POST.get('confirmar_password', '')
        
        if not all([codigo, nueva_password, confirmar_password]):
            messages.error(request, 'Todos los campos son obligatorios')
            return render(request, 'auth/verificar_codigo_recuperacion.html')
        
        if nueva_password != confirmar_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'auth/verificar_codigo_recuperacion.html')
        
        if len(nueva_password) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres')
            return render(request, 'auth/verificar_codigo_recuperacion.html')
        
        # Verificar código
        try:
            codigo_obj = CodigoVerificacion.objects.get(
                usuario=usuario,
                codigo=codigo,
                tipo='recuperacion',
                usado=False,
                fecha_expiracion__gt=timezone.now()
            )
            
            # Actualizar contraseña
            usuario.password = make_password(nueva_password)
            usuario.save()
            
            # Marcar código como usado
            codigo_obj.usado = True
            codigo_obj.save()
            
            # Registrar evento
            EventoSeguridad.objects.create(
                usuario=usuario,
                tipo_evento='cambio_password',
                descripcion='Contraseña cambiada exitosamente',
                ip_address=get_client_ip(request)
            )
            
            # Limpiar sesión
            request.session.pop('recuperacion_usuario_id', None)
            
            messages.success(request, 'Contraseña actualizada exitosamente. Ya puede iniciar sesión.')
            return redirect('login_usuario')
            
        except CodigoVerificacion.DoesNotExist:
            messages.error(request, 'Código incorrecto o expirado')
    
    return render(request, 'auth/verificar_codigo_recuperacion.html')


def logout_usuario(request):
    """Cerrar sesión del usuario"""
    request.session.flush()
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('verificar_usuario')


def consulta_planillas(request):
    """Vista protegida para consulta de planillas"""
    usuario_id = request.session.get('usuario_logueado')
    
    if not usuario_id:
        messages.warning(request, 'Debe iniciar sesión para acceder a esta sección')
        return redirect('login_usuario')
    
    try:
        usuario = UsuarioRegistrado.objects.get(id_usuario=usuario_id)
        return render(request, 'auth/consulta_planillas.html', {'usuario': usuario})
    except UsuarioRegistrado.DoesNotExist:
        return redirect('login_usuario')
