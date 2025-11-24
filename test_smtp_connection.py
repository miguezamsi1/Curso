"""
Script de diagnóstico detallado de conexión SMTP
Prueba la conexión paso a paso con el servidor de correo
"""

import os
import sys
import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('.env')

# Configuración desde .env
EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')

print("=" * 70)
print("DIAGNÓSTICO COMPLETO DE CONEXIÓN SMTP")
print("=" * 70)

print("\n📋 CONFIGURACIÓN:")
print(f"  Servidor: {EMAIL_HOST}")
print(f"  Puerto: {EMAIL_PORT}")
print(f"  Usuario: {EMAIL_HOST_USER}")
print(f"  Contraseña: {'*' * len(EMAIL_HOST_PASSWORD)}")
print(f"  TLS: {EMAIL_USE_TLS}")

# Paso 1: Resolver DNS
print("\n" + "=" * 70)
print("PASO 1: RESOLUCIÓN DNS")
print("=" * 70)
try:
    ip_address = socket.gethostbyname(EMAIL_HOST)
    print(f"✅ DNS resuelto correctamente")
    print(f"   {EMAIL_HOST} -> {ip_address}")
except socket.gaierror as e:
    print(f"❌ Error resolviendo DNS: {e}")
    sys.exit(1)

# Paso 2: Conexión TCP
print("\n" + "=" * 70)
print("PASO 2: CONEXIÓN TCP AL SERVIDOR")
print("=" * 70)
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    result = sock.connect_ex((EMAIL_HOST, EMAIL_PORT))
    sock.close()
    
    if result == 0:
        print(f"✅ Puerto {EMAIL_PORT} está abierto y aceptando conexiones")
    else:
        print(f"❌ No se puede conectar al puerto {EMAIL_PORT}")
        print(f"   Código de error: {result}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Error en conexión TCP: {e}")
    sys.exit(1)

# Paso 3: Conexión SMTP
print("\n" + "=" * 70)
print("PASO 3: CONEXIÓN SMTP")
print("=" * 70)
try:
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=10)
    server.set_debuglevel(1)  # Mostrar debug completo
    print("\n✅ Conexión SMTP establecida")
    
    # Paso 4: STARTTLS
    if EMAIL_USE_TLS:
        print("\n" + "=" * 70)
        print("PASO 4: INICIANDO TLS")
        print("=" * 70)
        server.starttls()
        print("✅ TLS iniciado correctamente")
    
    # Paso 5: Autenticación
    print("\n" + "=" * 70)
    print("PASO 5: AUTENTICACIÓN")
    print("=" * 70)
    try:
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        print("✅ Autenticación exitosa")
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Error de autenticación: {e}")
        print("\n🔍 POSIBLES CAUSAS:")
        print("   1. Usuario o contraseña incorrectos")
        print("   2. El servidor requiere autenticación diferente")
        print("   3. La cuenta está bloqueada o deshabilitada")
        server.quit()
        sys.exit(1)
    
    # Paso 6: Envío de prueba
    print("\n" + "=" * 70)
    print("PASO 6: ENVIANDO EMAIL DE PRUEBA")
    print("=" * 70)
    
    # Email de destino por defecto
    destinatario = "mzambrano@eea.gob.ec"
    print(f"\n📧 Enviando a: {destinatario}")
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = destinatario
    msg['Subject'] = 'Prueba de Conexión SMTP - EEA'
    
    body = f"""
    Este es un email de prueba del sistema EEA.
    
    Configuración utilizada:
    - Servidor: {EMAIL_HOST}
    - Puerto: {EMAIL_PORT}
    - TLS: {EMAIL_USE_TLS}
    
    Si recibe este mensaje, la configuración SMTP está funcionando correctamente.
    
    Fecha/Hora: {__import__('datetime').datetime.now()}
    """
    
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        server.send_message(msg)
        print(f"\n✅ Email enviado exitosamente a {destinatario}")
        print("\n📬 IMPORTANTE:")
        print("   - Revise la bandeja de entrada")
        print("   - Revise la carpeta de SPAM/Correo no deseado")
        print("   - Puede tardar unos minutos en llegar")
        
    except Exception as e:
        print(f"\n❌ Error al enviar: {e}")
        print(f"   Tipo: {type(e).__name__}")
    
    server.quit()
    print("\n✅ Conexión cerrada correctamente")
    
except smtplib.SMTPConnectError as e:
    print(f"❌ Error conectando al servidor SMTP: {e}")
except smtplib.SMTPException as e:
    print(f"❌ Error SMTP: {e}")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
    print(f"   Tipo: {type(e).__name__}")

print("\n" + "=" * 70)
print("DIAGNÓSTICO COMPLETADO")
print("=" * 70)
