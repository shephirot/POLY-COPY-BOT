@echo off
REM Script de instalación para Windows

echo 🐍 Instalando bot de copy trading de Polymarket (Python)
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado
    echo Por favor instala Python 3.8 o superior desde:
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python encontrado
python --version

REM Verificar si pip está instalado
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip no está instalado
    pause
    exit /b 1
)

echo ✓ pip encontrado
pip --version
echo.

REM Instalar dependencias
echo 📦 Instalando dependencias...
pip install -r ..\requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ Error en la instalación
    pause
    exit /b 1
)

echo.
echo ✅ Instalación completada!
echo.
echo Siguiente paso:
echo 1. Copia y configura .env:
echo    copy ..\\.env.example ..\\.env
echo    notepad ..\\.env
echo.
echo 2. Ejecuta el bot:
echo    python main.py
echo.
pause
