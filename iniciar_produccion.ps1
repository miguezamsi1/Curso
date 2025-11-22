# Script PowerShell para iniciar el servidor de producción

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Iniciando servidor EEA (Produccion)  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activar entorno virtual
& .\venv\Scripts\Activate.ps1

Write-Host "[1/4] Aplicando migraciones..." -ForegroundColor Yellow
python manage.py migrate

Write-Host ""
Write-Host "[2/4] Recopilando archivos estaticos..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

Write-Host ""
Write-Host "[3/4] Instalando waitress (servidor WSGI para Windows)..." -ForegroundColor Yellow
pip install waitress -q

Write-Host ""
Write-Host "[4/4] Iniciando servidor de produccion..." -ForegroundColor Green
Write-Host ""
Write-Host "Servidor disponible en http://localhost:8000" -ForegroundColor Green
Write-Host "Panel de administracion: http://localhost:8000/admin/" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

waitress-serve --port=8000 eea.wsgi:application
