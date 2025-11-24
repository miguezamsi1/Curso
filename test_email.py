"""
Script de prueba de configuración de correo electrónico
Ejecutar: python test_email.py
"""

import os
import sys
import django

# Configurar Django
sys.path.append(r'C:\Sistemas\eea')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eea.settings')
django.setup()

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def test_email_config():
    """Probar configuración de email"""
    
    print("=" * 60)
    print("PRUEBA DE CONFIGURACIÓN DE EMAIL")
    print("=" * 60)
    
    # Mostrar configuración actual
    print("\n📧 CONFIGURACIÓN ACTUAL:")
    print(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"  EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else '(vacío)'}")
    print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    print("\n" + "=" * 60)
    
    # Probar envío
    print("\n🔬 PROBANDO ENVÍO DE CORREO HTML...")
    
    email_destino = input("Ingrese email de destino para prueba: ")
    codigo_prueba = "123456"
    
    # Contenido texto plano
    text_content = f"""
    Estimado/a Usuario de Prueba,
    
    Este es un correo de prueba del sistema EEA.
    
    Su código de verificación de prueba es: {codigo_prueba}
    
    Configuración utilizada:
    - Servidor: {settings.EMAIL_HOST}
    - Puerto: {settings.EMAIL_PORT}
    - TLS: {settings.EMAIL_USE_TLS}
    
    Si recibe este mensaje, la configuración está funcionando correctamente.
    
    Atentamente,
    Empresa Eléctrica Azogues
    """
    
    # Contenido HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Prueba de Email - EEA</title>
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
            .codigo {{ 
                background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                border: 3px solid #2196f3; 
                padding: 30px; 
                text-align: center; 
                margin: 30px 0; 
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(33, 150, 243, 0.2);
            }}
            .codigo-numero {{ 
                font-size: 42px; 
                font-weight: bold; 
                color: #0d47a1; 
                letter-spacing: 10px;
                font-family: 'Courier New', monospace;
                text-shadow: 2px 2px 4px rgba(13, 71, 161, 0.2);
            }}
            .success-box {{
                background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
                border-left: 5px solid #4caf50;
                padding: 20px 25px;
                margin: 25px 0;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(76, 175, 80, 0.1);
            }}
            .info-table {{
                width: 100%;
                margin: 25px 0;
                border-collapse: collapse;
                background: #f8f9fa;
                border-radius: 10px;
                overflow: hidden;
            }}
            .info-table td {{
                padding: 15px;
                border-bottom: 1px solid #e0e0e0;
            }}
            .info-table tr:last-child td {{
                border-bottom: none;
            }}
            .info-table td:first-child {{
                font-weight: bold;
                color: #0066cc;
                width: 40%;
                background: #e3f2fd;
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
            .footer-contact {{
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid rgba(255,255,255,0.3);
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="email-wrapper">
            <div class="container">
                <div class="header">
                    <div class="header-icon">⚡</div>
                    <h1>EMPRESA ELÉCTRICA AZOGUES C.A.</h1>
                    <p>Prueba de Configuración de Email</p>
                    <div class="header-divider"></div>
                </div>
                <div class="content">
                    <p style="font-size: 18px; color: #0066cc; font-weight: 600; margin-bottom: 20px;">
                        Estimado/a Usuario de Prueba,
                    </p>
                    <p style="font-size: 16px; color: #555;">
                        Este es un correo de prueba para verificar que la configuración SMTP está funcionando correctamente.
                    </p>
                    
                    <div class="codigo">
                        <p style="margin: 0 0 15px 0; color: #1976d2; font-size: 15px; text-transform: uppercase; letter-spacing: 2px; font-weight: 700;">
                            🔐 Código de verificación de prueba:
                        </p>
                        <div class="codigo-numero">{codigo_prueba}</div>
                    </div>
                    
                    <div class="success-box">
                        <strong style="font-size: 16px; color: #2e7d32;">✅ Configuración Exitosa</strong><br>
                        <span style="color: #558b2f;">
                            Si está viendo este mensaje, la configuración de correo electrónico está funcionando correctamente.
                        </span>
                    </div>
                    
                    <h3 style="color: #0066cc; margin-top: 35px; margin-bottom: 20px; font-size: 20px;">
                        📋 Configuración Utilizada
                    </h3>
                    <table class="info-table">
                        <tr>
                            <td>🖥️ Servidor SMTP</td>
                            <td>{settings.EMAIL_HOST}</td>
                        </tr>
                        <tr>
                            <td>🔌 Puerto</td>
                            <td>{settings.EMAIL_PORT}</td>
                        </tr>
                        <tr>
                            <td>🔒 TLS Habilitado</td>
                            <td>{'✓ Sí' if settings.EMAIL_USE_TLS else '✗ No'}</td>
                        </tr>
                        <tr>
                            <td>👤 Usuario</td>
                            <td>{settings.EMAIL_HOST_USER}</td>
                        </tr>
                    </table>
                    
                    <div style="margin-top: 35px; padding-top: 25px; border-top: 2px solid #e0e0e0; text-align: center;">
                        <p style="font-size: 16px; color: #0066cc; font-weight: 600; margin: 5px 0;">
                            Atentamente,
                        </p>
                        <p style="font-size: 18px; color: #0d47a1; font-weight: bold; margin: 5px 0;">
                            Empresa Eléctrica Azogues C.A.
                        </p>
                        <p style="font-size: 14px; color: #666; margin: 5px 0;">
                            Jefatura de Sistemas
                        </p>
                    </div>
                </div>
                <div class="footer">
                    <p><strong style="font-size: 14px;">📧 Este es un correo automático de prueba</strong></p>
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
        # Crear mensaje con versiones texto y HTML
        email_msg = EmailMultiAlternatives(
            subject='CORREO EMPRESA ELECTRICA AZOGUES C.A.',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email_destino]
        )
        email_msg.attach_alternative(html_content, "text/html")
        
        print("\n📤 Intentando enviar email...")
        email_msg.send(fail_silently=False)
        print("✅ ¡EMAIL ENVIADO EXITOSAMENTE!")
        print(f"\n📬 Revise la bandeja de entrada de {email_destino}")
        print("   (También revise spam/correo no deseado)")
        
    except Exception as e:
        print(f"\n❌ ERROR AL ENVIAR EMAIL:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensaje: {str(e)}")
        
        # Analizar el error
        error_str = str(e).lower()
        
        if 'authentication' in error_str or 'username' in error_str or 'password' in error_str:
            print("\n🔐 PROBLEMA DE AUTENTICACIÓN:")
            print("   - Credenciales incorrectas")
            print("   - Verificar usuario y contraseña en .env")
            
        elif 'connection' in error_str or 'timeout' in error_str:
            print("\n🌐 PROBLEMA DE CONEXIÓN:")
            print("   - Firewall bloqueando puerto 587")
            print("   - Servidor SMTP no accesible")
        
    print("\n" + "=" * 60)

if __name__ == '__main__':
    test_email_config()
