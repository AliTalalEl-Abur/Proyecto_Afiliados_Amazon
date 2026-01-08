# 🚀 Guía de Configuración Rápida

## ⚡ Inicio Rápido (5 minutos)

### 1️⃣ Clonar o inicializar repositorio

```bash
# Si es nuevo proyecto
git init
git add .
git commit -m "Initial commit: MVP estructura base"

# Si clonas desde GitHub
git clone tu-repositorio-url
cd Proyecto_Afiliados_Amazon
```

### 2️⃣ Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env (copiar desde .env.example)
copy .env.example .env
```

**IMPORTANTE**: Edita `.env` y añade tu `OPENAI_API_KEY`

### 3️⃣ Configurar Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Crear archivo .env
copy .env.example .env
```

### 4️⃣ Ejecutar el Proyecto

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### 5️⃣ Verificar

- Backend: http://localhost:8000 (verás `{"message": "API de Ayuda Técnica funcionando"}`)
- Frontend: http://localhost:3000 (verás la página React)
- API Docs: http://localhost:8000/docs (documentación automática de FastAPI)

## 🔑 Obtener API Key de OpenAI

1. Ve a: https://platform.openai.com/api-keys
2. Crea una cuenta o inicia sesión
3. Clic en "Create new secret key"
4. Copia la key (empieza con `sk-...`)
5. Pégala en tu archivo `.env`:
   ```
   OPENAI_API_KEY=sk-tu-key-aqui
   ```

## 🐛 Solución de Problemas

### Error: "No module named 'fastapi'"
```bash
cd backend
pip install -r requirements.txt
```

### Error: "npm: command not found"
Instala Node.js desde: https://nodejs.org/

### Error: Puerto 8000 en uso
Cambia el puerto en `backend/.env`:
```
PORT=8001
```

### Error: CORS policy
Verifica que `CORS_ORIGINS` en `.env` incluya tu URL del frontend.

## 📝 Comandos Útiles

```bash
# Ver documentación API
http://localhost:8000/docs

# Ejecutar tests (cuando los tengas)
pytest

# Limpiar caché Python
find . -type d -name __pycache__ -exec rm -rf {} +

# Reconstruir node_modules
cd frontend && rm -rf node_modules && npm install
```

## ✅ Checklist de Configuración

- [ ] Python 3.9+ instalado
- [ ] Node.js 16+ instalado
- [ ] Git configurado
- [ ] Backend con venv creado
- [ ] Dependencias Python instaladas
- [ ] Dependencias npm instaladas
- [ ] Archivo `.env` creado con OPENAI_API_KEY
- [ ] Backend corriendo en :8000
- [ ] Frontend corriendo en :3000
- [ ] Repositorio Git inicializado

## 🎯 Siguiente Paso

Una vez todo funcione, continúa con la **Fase 1** para implementar la generación de artículos con LangChain.
