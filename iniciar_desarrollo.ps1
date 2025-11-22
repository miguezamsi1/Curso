# Script PowerShell para iniciar el servidor de desarrollo Django

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Iniciando servidor EEA (Desarrollo)  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activar entorno virtual
& .\venv\Scripts\Activate.ps1

Write-Host "[1/2] Aplicando migraciones..." -ForegroundColor Yellow
python manage.py migrate

Write-Host ""
Write-Host "[2/2] Iniciando servidor de desarrollo en http://localhost:8000" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver 0.0.0.0:8000
