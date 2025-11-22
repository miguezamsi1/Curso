@echo off
REM Script para iniciar el servidor de desarrollo Django

echo ========================================
echo    Iniciando servidor EEA (Desarrollo)
echo ========================================
echo.

REM Activar entorno virtual
call venv\Scripts\activate.bat

echo [1/2] Aplicando migraciones...
python manage.py migrate

echo.
echo [2/2] Iniciando servidor de desarrollo en http://localhost:8000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python manage.py runserver 0.0.0.0:8000
