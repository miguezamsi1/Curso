@echo off
REM Script para iniciar el servidor de producción con Gunicorn

echo ========================================
echo    Iniciando servidor EEA (Produccion)
echo ========================================
echo.

REM Activar entorno virtual
call venv\Scripts\activate.bat

echo [1/3] Aplicando migraciones...
python manage.py migrate

echo.
echo [2/3] Recopilando archivos estaticos...
python manage.py collectstatic --noinput

echo.
echo [3/3] Iniciando servidor Gunicorn...
echo.
echo Servidor disponible en http://localhost:8000
echo Presiona Ctrl+C para detener el servidor
echo.

REM Gunicorn no funciona nativamente en Windows, usar waitress en su lugar
pip install waitress >nul 2>&1
waitress-serve --port=8000 eea.wsgi:application
