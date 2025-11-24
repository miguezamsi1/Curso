"""
Script para probar el envío real de correo desde la aplicación
"""
import os
import sys
import django

# Configurar Django
sys.path.append(r'C:\Sistemas\eea')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eea.settings')
django.setup()

from appeea.views_auth import enviar_email_verificacion

# Datos de prueba
email_destino = "mzambrano@eea.gob.ec"
codigo_prueba = "123456"
nombre_prueba = "MIGUEL NESTOR"

print("=" * 70)
print("PRUEBA REAL DE ENVÍO DE CORREO CON LOGO")
print("=" * 70)
print(f"\n📧 Destinatario: {email_destino}")
print(f"🔐 Código: {codigo_prueba}")
print(f"👤 Nombre: {nombre_prueba}")
print("\n📤 Enviando correo con logo embebido...")

# Enviar correo
resultado = enviar_email_verificacion(email_destino, codigo_prueba, nombre_prueba)

if resultado:
    print("\n✅ ¡CORREO ENVIADO EXITOSAMENTE!")
    print(f"\n📬 Revise la bandeja de {email_destino}")
    print("   - Debe ver el logo de la empresa en el header")
    print("   - Fondo gris claro (sin morado)")
    print("   - Subject: CORREO EMPRESA ELECTRICA AZOGUES C.A.")
    print("   - Contacto: info@eea.gob.ec")
    print("   - Teléfono: (07) 2240377")
    print("   - Jefatura de Sistemas")
else:
    print("\n❌ ERROR: No se pudo enviar el correo")

print("\n" + "=" * 70)
