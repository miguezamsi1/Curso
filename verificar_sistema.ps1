# Script de verificacion del sistema EEA

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Verificacion del Sistema EEA          " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Verificar Python
Write-Host "[1/8] Verificando Python..." -NoNewline
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3\.(1[3-9]|[2-9][0-9])") {
    Write-Host " OK ($pythonVersion)" -ForegroundColor Green
} else {
    Write-Host " FALLO (Se requiere Python 3.13+)" -ForegroundColor Red
    $allGood = $false
}

# Verificar entorno virtual
Write-Host "[2/8] Verificando entorno virtual..." -NoNewline
if (Test-Path "venv\Scripts\python.exe") {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " FALLO (Ejecutar: python -m venv venv)" -ForegroundColor Red
    $allGood = $false
}

# Activar entorno virtual
if (Test-Path "venv\Scripts\Activate.ps1") {
    & .\venv\Scripts\Activate.ps1 2>$null
}

# Verificar Django
Write-Host "[3/8] Verificando Django..." -NoNewline
$djangoVersion = python -c "import django; print(django.get_version())" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host " OK (v$djangoVersion)" -ForegroundColor Green
} else {
    Write-Host " FALLO" -ForegroundColor Red
    $allGood = $false
}

# Verificar base de datos
Write-Host "[4/8] Verificando base de datos..." -NoNewline
if (Test-Path "db.sqlite3") {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " WARNING (Ejecutar: python manage.py migrate)" -ForegroundColor Yellow
}

# Verificar migraciones
Write-Host "[5/8] Verificando migraciones..." -NoNewline
$output = python manage.py showmigrations --plan 2>&1 | Select-String "\[ \]"
if ($output) {
    Write-Host " WARNING (Hay migraciones pendientes)" -ForegroundColor Yellow
} else {
    Write-Host " OK" -ForegroundColor Green
}

# Verificar archivos estaticos
Write-Host "[6/8] Verificando archivos estaticos..." -NoNewline
if (Test-Path "staticfiles") {
    $staticCount = (Get-ChildItem -Path "staticfiles" -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
    if ($staticCount -gt 0) {
        Write-Host " OK ($staticCount archivos)" -ForegroundColor Green
    } else {
        Write-Host " WARNING (Ejecutar: python manage.py collectstatic)" -ForegroundColor Yellow
    }
} else {
    Write-Host " WARNING (Ejecutar: python manage.py collectstatic)" -ForegroundColor Yellow
}

# Verificar dependencias
Write-Host "[7/8] Verificando dependencias clave..." -NoNewline
$requiredPackages = @("django-ckeditor", "Pillow", "whitenoise", "requests")
$missingPackages = @()
foreach ($package in $requiredPackages) {
    $installed = pip show $package 2>&1 | Select-String "Name:"
    if (-not $installed) {
        $missingPackages += $package
    }
}
if ($missingPackages.Count -eq 0) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " FALLO (Faltantes: $($missingPackages -join ', '))" -ForegroundColor Red
    $allGood = $false
}

# Verificar configuracion Django
Write-Host "[8/8] Verificando configuracion Django..." -NoNewline
$checkOutput = python manage.py check 2>&1
if ($checkOutput -match "System check identified no issues") {
    Write-Host " OK" -ForegroundColor Green
} elseif ($checkOutput -match "0 silenced") {
    Write-Host " OK (con warnings)" -ForegroundColor Yellow
} else {
    Write-Host " FALLO" -ForegroundColor Red
    $allGood = $false
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "  Sistema listo para usar             " -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Proximos pasos:" -ForegroundColor Yellow
    Write-Host "1. Crear superusuario: python manage.py createsuperuser"
    Write-Host "2. Iniciar servidor: .\iniciar_desarrollo.ps1"
} else {
    Write-Host "  Hay problemas que resolver           " -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Revisa los errores arriba y corrígelos antes de continuar." -ForegroundColor Yellow
}

Write-Host ""
