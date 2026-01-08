#!/bin/bash
# Script de inicio rápido para el proyecto

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     🚀 PROYECTO AFILIADOS AMAZON - INICIO RÁPIDO          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Detectar SO
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    OS="Windows"
    PYTHON_CMD="python"
    ACTIVATE_CMD="venv\\Scripts\\activate"
else
    OS="Unix"
    PYTHON_CMD="python3"
    ACTIVATE_CMD="source venv/bin/activate"
fi

echo -e "${BLUE}[1/5] Verificando requisitos previos...${NC}"
echo ""

# Verificar Python
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo -e "${RED}❌ Python no está instalado${NC}"
    echo "Descarga desde: https://www.python.org/downloads/"
    exit 1
fi
echo -e "${GREEN}✓ Python encontrado: $(python --version)${NC}"

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js no está instalado${NC}"
    echo "Descarga desde: https://nodejs.org/"
    exit 1
fi
echo -e "${GREEN}✓ Node.js encontrado: $(node --version)${NC}"

# Verificar Git
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git no está instalado${NC}"
    echo "Descarga desde: https://git-scm.com/"
    exit 1
fi
echo -e "${GREEN}✓ Git encontrado: $(git --version)${NC}"

echo ""
echo -e "${BLUE}[2/5] Configurando Backend...${NC}"
echo ""

cd backend

# Crear virtual environment si no existe
if [ ! -d "venv" ]; then
    echo "Creando virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activar venv
echo "Activando virtual environment..."
eval $ACTIVATE_CMD

# Instalar dependencias
echo "Instalando dependencias Python..."
pip install -r requirements.txt -q

# Crear .env si no existe
if [ ! -f ".env" ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Archivo .env no encontrado${NC}"
    echo "Por favor, crea backend/.env con:"
    echo ""
    echo "OPENAI_API_KEY=sk-proj-tu-clave-aqui"
    echo "WORDPRESS_URL=https://tudominio.com"
    echo "WORDPRESS_USER=usuario"
    echo "WORDPRESS_APP_PASSWORD=contraseña"
    echo "AMAZON_AFFILIATE_TAG=tutorial-21"
    echo "CORS_ORIGINS=http://localhost:3000"
    echo ""
    echo -e "${BLUE}Presiona Enter para continuar...${NC}"
    read
fi

cd ..

echo ""
echo -e "${BLUE}[3/5] Configurando Frontend...${NC}"
echo ""

cd frontend

# Instalar dependencias de Node
echo "Instalando dependencias Node.js..."
npm install -q

cd ..

echo ""
echo -e "${BLUE}[4/5] Verificando estructura...${NC}"
echo ""

# Verificar directorios
dirs=("backend" "frontend" "backend/agents")
for dir in "${dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓ Directorio $dir encontrado${NC}"
    else
        echo -e "${RED}✗ Directorio $dir no encontrado${NC}"
        exit 1
    fi
done

echo ""
echo -e "${BLUE}[5/5] Listo para iniciar!${NC}"
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║               🎉 SETUP COMPLETADO CON ÉXITO               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}Para iniciar el proyecto, abre 2 terminales:${NC}"
echo ""
echo -e "${YELLOW}Terminal 1 (Backend):${NC}"
echo "  cd backend"
if [[ "$OS" == "Windows" ]]; then
    echo "  venv\\Scripts\\activate"
else
    echo "  source venv/bin/activate"
fi
echo "  python -m uvicorn main:app --reload"
echo ""
echo -e "${YELLOW}Terminal 2 (Frontend):${NC}"
echo "  cd frontend"
echo "  npm start"
echo ""
echo -e "${BLUE}Luego abre en tu navegador:${NC}"
echo "  Frontend: http://localhost:3000"
echo "  Backend: http://localhost:8000"
echo "  Docs API: http://localhost:8000/docs"
echo ""
echo "📖 Lee la documentación:"
echo "  - README_COMPLETO.md"
echo "  - FASE_4.md"
echo "  - SETUP.md"
echo ""
