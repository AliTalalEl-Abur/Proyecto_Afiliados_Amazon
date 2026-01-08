@echo off
REM Script de inicio rápido para Windows

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     🚀 PROYECTO AFILIADOS AMAZON - INICIO RÁPIDO          ║
echo ║                    WINDOWS VERSION                         ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Colores
setlocal enabledelayedexpansion

echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado
    echo Descarga desde: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✓ Python encontrado

echo.
echo [2/4] Configurando Backend...
cd backend

REM Crear venv si no existe
if not exist "venv" (
    echo Creando virtual environment...
    python -m venv venv
)

REM Activar venv
echo Activando virtual environment...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo Instalando dependencias Python...
pip install -r requirements.txt -q

REM Verificar .env
if not exist ".env" (
    echo.
    echo ⚠️  Archivo .env no encontrado
    echo Por favor, crea backend\.env con:
    echo.
    echo OPENAI_API_KEY=sk-proj-tu-clave-aqui
    echo WORDPRESS_URL=https://tudominio.com
    echo WORDPRESS_USER=usuario
    echo WORDPRESS_APP_PASSWORD=contraseña
    echo AMAZON_AFFILIATE_TAG=tutorial-21
    echo CORS_ORIGINS=http://localhost:3000
    echo.
    pause
)

cd ..

echo.
echo [3/4] Configurando Frontend...
cd frontend
echo Instalando dependencias Node.js...
call npm install -q
cd ..

echo.
echo [4/4] Verificando estructura...
if exist "backend" echo ✓ Backend encontrado
if exist "frontend" echo ✓ Frontend encontrado
if exist "backend\agents" echo ✓ Agents encontrados

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║               🎉 SETUP COMPLETADO CON ÉXITO               ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Para iniciar el proyecto, abre 2 Command Prompts:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   venv\Scripts\activate
echo   python -m uvicorn main:app --reload
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm start
echo.
echo Luego abre en tu navegador:
echo   Frontend: http://localhost:3000
echo   Backend: http://localhost:8000
echo   Docs API: http://localhost:8000/docs
echo.
echo 📖 Lee la documentación:
echo   - README_COMPLETO.md
echo   - FASE_4.md
echo   - SETUP.md
echo.
pause
