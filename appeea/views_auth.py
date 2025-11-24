# -*- coding: utf-8 -*-
"""
Vistas para el Módulo de Registro y Verificación de Usuarios
Sistema de autenticación corporativo EEA
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
import random
import string
import logging

from .models import UsuarioRegistrado, CodigoVerificacion, EventoSeguridad

# Logger para emails
logger = logging.getLogger('django.core.mail')


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
    """Envía email con código de verificación en formato HTML profesional"""
    subject = 'CORREO EMPRESA ELECTRICA AZOGUES C.A.'
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', settings.EMAIL_HOST_USER)
    
    # Versión texto plano (fallback)
    text_content = f"""
    Estimado/a {nombres},
    
    Ha solicitado un código de verificación para acceder al sistema de la Empresa Eléctrica Azogues.
    
    Su código de verificación es: {codigo}
    
    ⏰ IMPORTANTE: Este código es válido por 15 minutos.
    
    Si usted no solicitó este código, por favor ignore este mensaje.
    
    Atentamente,
    Empresa Eléctrica Azogues
    
    ---
    Este es un correo automático, por favor no responder.
    © 2025 Empresa Eléctrica Azogues - Todos los derechos reservados
    """
    
    # Versión HTML (mejorada)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Código de Verificación - EEA</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6; 
                color: #333; 
                background: #f5f5f5;
                margin: 0;
                padding: 0;
            }}
            .email-wrapper {{
                width: 100%;
                background: #f5f5f5;
                padding: 40px 20px;
            }}
            .container {{ 
                max-width: 600px; 
                margin: 0 auto; 
                background-color: #ffffff;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            }}
            .header {{ 
                background: linear-gradient(135deg, #0066cc 0%, #00b4d8 50%, #40a9ff 100%);
                color: white; 
                padding: 50px 30px; 
                text-align: center;
                position: relative;
                overflow: hidden;
            }}
            .header::before {{
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                animation: pulse 4s ease-in-out infinite;
            }}
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); opacity: 0.5; }}
                50% {{ transform: scale(1.1); opacity: 0.8; }}
            }}
            .header-icon {{
                font-size: 64px;
                margin-bottom: 15px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                animation: glow 2s ease-in-out infinite;
            }}
            @keyframes glow {{
                0%, 100% {{ text-shadow: 0 0 10px rgba(255,255,255,0.5), 0 0 20px rgba(255,255,255,0.3); }}
                50% {{ text-shadow: 0 0 20px rgba(255,255,255,0.8), 0 0 30px rgba(255,255,255,0.5); }}
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: bold;
                position: relative;
                z-index: 1;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }}
            .header p {{
                margin: 10px 0 0 0;
                font-size: 16px;
                opacity: 0.95;
                position: relative;
                z-index: 1;
                font-weight: 500;
            }}
            .header-divider {{
                height: 4px;
                background: linear-gradient(90deg, transparent 0%, #ffffff 50%, transparent 100%);
                margin-top: 20px;
            }}
            .content {{ 
                background: #ffffff; 
                padding: 40px 30px;
            }}
            .greeting {{
                font-size: 18px;
                margin-bottom: 20px;
                color: #0066cc;
                font-weight: 600;
            }}
            .codigo {{ 
                background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                border: 3px solid #2196f3; 
                padding: 30px; 
                text-align: center; 
                margin: 30px 0; 
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(33, 150, 243, 0.2);
            }}
            .codigo-label {{
                margin: 0 0 15px 0; 
                color: #1976d2; 
                font-size: 15px;
                text-transform: uppercase;
                letter-spacing: 2px;
                font-weight: 700;
            }}
            .codigo-numero {{ 
                font-size: 42px; 
                font-weight: bold; 
                color: #0d47a1; 
                letter-spacing: 10px;
                font-family: 'Courier New', monospace;
                text-shadow: 2px 2px 4px rgba(13, 71, 161, 0.2);
            }}
            .warning {{ 
                background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
                border-left: 5px solid #ff9800; 
                padding: 20px 25px; 
                margin: 25px 0;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(255, 152, 0, 0.1);
            }}
            .warning strong {{
                color: #e65100;
                font-size: 16px;
            }}
            .info-box {{
                background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
                border-left: 5px solid #4caf50;
                padding: 15px 20px;
                margin: 20px 0;
                border-radius: 8px;
            }}
            .footer {{ 
                background: linear-gradient(135deg, #0066cc 0%, #00b4d8 100%);
                padding: 30px 20px; 
                text-align: center; 
                color: white;
            }}
            .footer p {{
                margin: 8px 0;
                font-size: 13px;
            }}
            .footer strong {{
                font-size: 14px;
            }}
            .footer-contact {{
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid rgba(255,255,255,0.3);
                font-size: 12px;
                opacity: 0.9;
            }}
            .signature {{
                margin-top: 35px;
                padding-top: 25px;
                border-top: 2px solid #e0e0e0;
                text-align: center;
            }}
            .signature p {{
                margin: 5px 0;
                line-height: 1.8;
            }}
        </style>
    </head>
    <body>
        <div class="email-wrapper">
            <div class="container">
                <div class="header">
                    <div class="header-icon">
                        <img src="cid:logo_eea" alt="EEA Logo" style="width: 80px; height: 80px; margin-bottom: 10px; border-radius: 50%; background: white; padding: 5px;">
                    </div>
                    <h1>EMPRESA ELÉCTRICA AZOGUES C.A.</h1>
                    <p>Sistema de Verificación de Usuarios</p>
                    <div class="header-divider"></div>
                </div>
                <div class="content">
                    <p class="greeting">Estimado/a {nombres},</p>
                    <p style="font-size: 16px; color: #555;">
                        Ha solicitado un código de verificación para acceder al sistema de la 
                        <strong>Empresa Eléctrica Azogues</strong>.
                    </p>
                    
                    <div class="codigo">
                        <p class="codigo-label">🔐 Su código de verificación es:</p>
                        <div class="codigo-numero">{codigo}</div>
                    </div>
                    
                    <div class="warning">
                        <strong>⏰ Importante:</strong> Este código es válido por <strong>15 minutos</strong>. 
                        Por seguridad, no comparta este código con nadie.
                    </div>
                    
                    <div class="info-box">
                        <strong>✓ Consejo de Seguridad:</strong> Nunca comparta su código de verificación 
                        con terceros. La Empresa Eléctrica Azogues nunca le solicitará este código por teléfono o correo.
                    </div>
                    
                    <p style="margin-top: 25px; font-size: 15px; color: #666;">
                        Si usted no solicitó este código, por favor ignore este mensaje o 
                        contacte inmediatamente con el departamento de sistemas.
                    </p>
                    
                    <div class="signature">
                        <p style="font-size: 16px; color: #0066cc; font-weight: 600;">
                            Atentamente,
                        </p>
                        <p style="font-size: 18px; color: #0d47a1; font-weight: bold;">
                            Empresa Eléctrica Azogues C.A.
                        </p>
                        <p style="font-size: 14px; color: #666;">
                            Jefatura de Sistemas
                        </p>
                    </div>
                </div>
                <div class="footer">
                    <p><strong>📧 Este es un correo automático, por favor no responder</strong></p>
                    <p style="font-size: 14px; margin-top: 10px;">
                        © 2025 Empresa Eléctrica Azogues C.A. - Todos los derechos reservados
                    </p>
                    <div class="footer-contact">
                        <p>¿Necesita ayuda? Contacte a: <strong>info@eea.gob.ec</strong></p>
                        <p>📞 Teléfono: (07) 2240377 | 🌐 www.eea.gob.ec</p>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        # Crear mensaje con alternativas (texto plano + HTML)
        email_msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[email]
        )
        email_msg.attach_alternative(html_content, "text/html")
        
        # Adjuntar logo como imagen embebida
        import os
        from email.mime.image import MIMEImage
        
        logo_path = os.path.join(settings.BASE_DIR, 'media', 'logo', 'circulo.png')
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                logo_data = f.read()
                logo_image = MIMEImage(logo_data)
                logo_image.add_header('Content-ID', '<logo_eea>')
                logo_image.add_header('Content-Disposition', 'inline', filename='logo.png')
                email_msg.attach(logo_image)
        
        # Enviar
        email_msg.send(fail_silently=False)
        
        logger.info(f"Email de verificación enviado exitosamente a {email}")
        return True
        
    except Exception as e:
        logger.error(f"Error enviando email a {email}: {str(e)}")
        print(f"❌ Error enviando email: {e}")
        return False
    
    # Versión texto plano (fallback)
    text_content = f"""
    Estimado/a {nombres},
    
    Ha solicitado un código de verificación para acceder al sistema de la Empresa Eléctrica Azogues.
    
    Su código de verificación es: {codigo}
    
    ⏰ IMPORTANTE: Este código es válido por 15 minutos.
    
    Si usted no solicitó este código, por favor ignore este mensaje.
    
    Atentamente,
    Empresa Eléctrica Azogues
    
    ---
    Este es un correo automático, por favor no responder.
    © 2025 Empresa Eléctrica Azogues - Todos los derechos reservados
    """
    
    # Versión HTML (mejorada)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Código de Verificación - EEA</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6; 
                color: #333; 
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .email-wrapper {{
                width: 100%;
                background-color: #f4f4f4;
                padding: 20px 0;
            }}
            .container {{ 
                max-width: 600px; 
                margin: 0 auto; 
                background-color: #ffffff;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .header {{ 
                background: linear-gradient(135deg, #003D82 0%, #40A9E3 100%); 
                color: white; 
                padding: 30px 20px; 
                text-align: center; 
            }}
            .header h1 {{
                margin: 0;
                font-size: 26px;
                font-weight: bold;
            }}
            .header p {{
                margin: 8px 0 0 0;
                font-size: 14px;
                opacity: 0.9;
            }}
            .content {{ 
                background: #ffffff; 
                padding: 40px 30px;
            }}
            .greeting {{
                font-size: 16px;
                margin-bottom: 20px;
            }}
            .codigo {{ 
                background: #f8f9fa; 
                border: 2px dashed #003D82; 
                padding: 25px; 
                text-align: center; 
                margin: 30px 0; 
                border-radius: 10px;
            }}
            .codigo-label {{
                margin: 0 0 12px 0; 
                color: #666; 
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .codigo-numero {{ 
                font-size: 36px; 
                font-weight: bold; 
                color: #003D82; 
                letter-spacing: 8px;
                font-family: 'Courier New', monospace;
            }}
            .warning {{ 
                background: #FFF3E0; 
                border-left: 4px solid #FF9800; 
                padding: 15px 20px; 
                margin: 25px 0;
                border-radius: 4px;
            }}
            .warning strong {{
                color: #E65100;
            }}
            .footer {{ 
                background: #f8f9fa; 
                padding: 20px; 
                text-align: center; 
                font-size: 12px; 
                color: #666;
                border-top: 1px solid #e0e0e0;
            }}
            .footer p {{
                margin: 5px 0;
            }}
            .signature {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #e0e0e0;
            }}
        </style>
    </head>
    <body>
        <div class="email-wrapper">
            <div class="container">
                <div class="header">
                    <h1>⚡ Empresa Eléctrica Azogues</h1>
                    <p>Sistema de Verificación de Usuarios</p>
                </div>
                <div class="content">
                    <p class="greeting">Estimado/a <strong>{nombres}</strong>,</p>
                    <p>Ha solicitado un código de verificación para acceder al sistema de la Empresa Eléctrica Azogues.</p>
                    
                    <div class="codigo">
                        <p class="codigo-label">Su código de verificación es:</p>
                        <div class="codigo-numero">{codigo}</div>
                    </div>
                    
                    <div class="warning">
                        <strong>⏰ Importante:</strong> Este código es válido por <strong>15 minutos</strong>. 
                        Por seguridad, no comparta este código con nadie.
                    </div>
                    
                    <p>Si usted no solicitó este código, por favor ignore este mensaje o contacte con el departamento de sistemas.</p>
                    
                    <div class="signature">
                        <p>Atentamente,<br>
                        <strong>Empresa Eléctrica Azogues</strong><br>
                        Departamento de Sistemas</p>
                    </div>
                </div>
                <div class="footer">
                    <p><strong>Este es un correo automático, por favor no responder.</strong></p>
                    <p>© 2025 Empresa Eléctrica Azogues - Todos los derechos reservados</p>
                    <p style="margin-top: 10px; color: #999;">
                        Si tiene problemas, contacte a: sistemas@eea.gob.ec
                    </p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        # Crear mensaje con alternativas (texto plano + HTML)
        email_msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[email]
        )
        email_msg.attach_alternative(html_content, "text/html")
        
        # Enviar
        email_msg.send(fail_silently=False)
        
        logger.info(f"Email de verificación enviado exitosamente a {email}")
        return True
        
    except Exception as e:
        logger.error(f"Error enviando email a {email}: {str(e)}")
        print(f"❌ Error enviando email: {e}")
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
                messages.success(request, f'✉️ Correo enviado satisfactoriamente a: {usuario.email}')
                request.session['codigo_enviado'] = True
            else:
                messages.warning(request, f'⚠️ No fue posible enviar el correo a {usuario.email}. Por favor verifique su conexión o intente más tarde.')
        
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
                messages.success(request, f'✉️ Se ha enviado un código de verificación a {email}')
                return redirect('verificar_codigo_recuperacion')
            else:
                messages.warning(request, f'⚠️ No fue posible enviar el correo a {email}. Por favor verifique su conexión o intente más tarde.')
        
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
