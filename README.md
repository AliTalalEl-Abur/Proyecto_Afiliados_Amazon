# MVP Ayuda Técnica - Generación Automática de Artículos

Sistema de ayuda técnica con generación automática de contenido usando IA.

## 🎯 Stack Técnico

- **Backend**: FastAPI + Python
- **Frontend**: React 18
- **IA**: LangChain + GPT-4o (OpenAI)
- **Base de datos**: SQLite (migratable a Supabase)
- **Hosting**: VPS / Vercel

## 📁 Estructura del Proyecto

```
/backend          # API REST con FastAPI
  main.py         # Punto de entrada de la API
  requirements.txt
  /agents         # Agentes de generación de contenido
  
/frontend         # Aplicación React
  /src
  /public
  package.json
  
/shared           # Utilidades compartidas
  utils.py
```

## 🚀 Instalación y Configuración

### Backend

1. Crear entorno virtual:
```bash
cd backend
python -m venv venv
```

2. Activar entorno virtual:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
- Copiar `.env.example` a `.env`
- Añadir tu `OPENAI_API_KEY`

5. Ejecutar servidor:
```bash
python main.py
```

API disponible en: http://localhost:8000

### Frontend

1. Instalar dependencias:
```bash
cd frontend
npm install
```

2. Crear archivo `.env` en /frontend:
```
REACT_APP_API_URL=http://localhost:8000
```

3. Ejecutar aplicación:
```bash
npm start
```

Aplicación disponible en: http://localhost:3000

## 🔑 Configuración de OpenAI

1. Obtén tu API key en: https://platform.openai.com/api-keys
2. Añádela al archivo `.env` en la raíz del proyecto
3. Modelo recomendado: `gpt-4o` (más económico y rápido)

## 📝 Uso con GitHub

```bash
git init
git add .
git commit -m "Initial commit - MVP estructura base"
git branch -M main
git remote add origin tu-repositorio-url
git push -u origin main
```

## 🔄 Próximos Pasos (Roadmap)

- [ ] Fase 1: Implementar generador de artículos con LangChain
- [ ] Fase 2: Crear interfaz de usuario para generación
- [ ] Fase 3: Sistema de almacenamiento de artículos
- [ ] Fase 4: Optimización SEO automática
- [ ] Fase 5: Deploy en producción

## 🛠️ Desarrollo con Copilot

Este proyecto está optimizado para usar con GitHub Copilot. Abre el workspace en VS Code para obtener sugerencias inteligentes.

## 📄 Licencia

MIT
