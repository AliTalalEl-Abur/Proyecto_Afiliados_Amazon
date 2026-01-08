# FASE 3 - Integración con WordPress

## Configuración de WordPress

### Requisitos

1. **Sitio WordPress funcionando** (local o en servidor)
2. **Plugin de REST API habilitado** (incluido en WordPress 4.7+)
3. **Credenciales de usuario con permisos de administrador**

### Pasos de Configuración

#### 1. Crear usuario para API

En WordPress Admin:
1. Ve a **Usuarios** → **Añadir nuevo**
2. Crea un usuario (ej: `api_user`)
3. Asigna rol **Administrador** o **Editor**

#### 2. Generar App Password (Contraseña de Aplicación)

En WordPress Admin:
1. Ve a **Usuarios** → **Perfil** del usuario
2. Desplázate a **App Passwords**
3. Introduce un nombre (ej: "Generador Artículos")
4. Haz clic en **Crear Contraseña de Aplicación**
5. **Copia la contraseña generada** (formato: `xxxx-xxxx-xxxx-xxxx`)

#### 3. Configurar variables de entorno

En `backend/.env`:

```env
# Configuración de WordPress
WORDPRESS_URL=https://ejemplo.com
WORDPRESS_USER=api_user
WORDPRESS_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

**Ejemplo para WordPress local:**
```env
WORDPRESS_URL=http://localhost:8080
WORDPRESS_USER=admin
WORDPRESS_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

## Cómo funciona

### Flujo de Publicación

1. **Generar Artículo**
   - PDF → IA → Artículo estructurado
   
2. **Preparar para WordPress**
   - Convertir a HTML formateado
   - Añadir enlaces de afiliado
   - Preparar metadatos SEO

3. **Elegir Estado**
   - 📋 **Borrador**: Revisar antes de publicar
   - 🚀 **Publicado**: Disponible inmediatamente

4. **Publicar**
   - Crear categoría "Ayuda técnica" (si no existe)
   - Crear post con contenido HTML
   - Asignar metadatos (error, modelo, SEO)

### Características Automáticas

✅ **Formato HTML profesional**
- Headings estructurados (H1, H2, H3)
- Párrafos con estilos
- Listas y numeraciones
- Grid de productos responsive

✅ **Categorización automática**
- Crea categoría "Ayuda técnica" si no existe
- Asigna automáticamente los posts

✅ **Metadatos SEO**
- Descripción (excerpt) del artículo
- Metadatos personalizados:
  - `error_type`: Tipo de error
  - `device_model`: Modelo del dispositivo

✅ **Enlaces de Afiliado**
- Incluye URLs de Amazon con tu tag
- Formateados como botones clicables

## UI - Cómo Publicar

### Desde el Frontend

1. **Generar artículo** completando el formulario
2. **Revisar resultado** (título, contenido, productos)
3. **Hacer clic en "📝 WordPress"**
4. **Modal de publicación:**
   - Previsualización del artículo
   - Opción de Borrador o Publicado
   - Información que se publicará

### Opciones

- **Guardar como borrador**
  - Artículo disponible en WordPress
  - Puedes revisarlo y editarlo manualmente
  - No aparece en el sitio público
  
- **Publicar directamente**
  - Artículo se publica inmediatamente
  - Visible en el sitio público
  - Aparece en el blog y búsqueda

## Ejemplo Práctico

### Paso a paso

1. **Preparar PDF**
   - Descarga manual técnico (ej: Alexa Echo Dot)
   - Súbelo a un servidor o usa URL pública

2. **Configurar WordPress**
   - Instala WordPress localmente o en servidor
   - Crea usuario con App Password
   - Añade credenciales en `backend/.env`

3. **Generar artículo**
   - Abre http://localhost:3000
   - Completa:
     - URL del PDF
     - Error: "Error E03 - Fallo de comunicación"
     - Modelo: "Amazon Echo Dot 4"
   - Clic en "Generar artículo"

4. **Publicar**
   - Espera a que se genere el artículo
   - Revisa contenido
   - Clic en "📝 WordPress"
   - Elige **"Guardar como borrador"**
   - Clic en "Guardar en WordPress"

5. **Revisar en WordPress**
   - Ve a http://localhost:8080/wp-admin
   - Entrar como `api_user`
   - Revisa el post en **Posts → Todos**
   - Ajusta si es necesario
   - Publica cuando esté listo

## Troubleshooting

### Error: "WordPress no está configurado"

**Causa:** Variables de entorno no configuradas

**Solución:**
```bash
# Verifica que backend/.env tiene:
cat backend/.env | grep WORDPRESS
```

### Error: "Unauthorized" (401)

**Causa:** Credenciales incorrectas

**Solución:**
1. Verifica que el usuario existe en WordPress
2. Confirma que el App Password es correcto
3. Prueba en Postman:
```bash
curl -u api_user:xxxx-xxxx-xxxx-xxxx https://ejemplo.com/wp-json/wp/v2/posts
```

### Error: "Forbidden" (403)

**Causa:** Usuario sin permisos

**Solución:**
1. Ve a WordPress → Usuarios
2. Asigna rol **Administrador** al usuario

### Artículo no aparece

**Causa:** Posible limitación de CORS

**Solución:**
1. Verifica que WORDPRESS_URL es accesible desde tu máquina
2. Si es local, usa `http://localhost:PUERTO`
3. No uses `https://localhost` para desarrollo local

## API Endpoints

### Publicar Artículo

```bash
POST /publish_to_wordpress

Body:
{
  "title": "Cómo solucionar Error E03",
  "content": {
    "introduction": "...",
    "error_meaning": "...",
    "diagnosis": "...",
    "solution_steps": [...],
    "common_failures": [...]
  },
  "affiliate_links": [
    {"name": "Multímetro", "type": "herramienta", ...}
  ],
  "error": "Error E03",
  "model": "Echo Dot 4",
  "status": "draft"
}

Response:
{
  "success": true,
  "post_id": 123,
  "url": "https://ejemplo.com/ayuda-tecnica/error-e03/",
  "status": "draft",
  "message": "Artículo guardado como borrador exitosamente"
}
```

## Próximos Pasos

- [ ] Integrar plugin de SEO (Yoast)
- [ ] Scheduled publishing (publicar en fecha/hora específica)
- [ ] Actualizar posts existentes
- [ ] Sincronizar imágenes featured
- [ ] Historial de publicaciones

## Recursos

- [WordPress REST API Documentation](https://developer.wordpress.org/rest-api/)
- [App Passwords Documentation](https://make.wordpress.org/plugins/2020/12/01/application-passwords-integration-in-docker-wordpress/)
- [WordPress Security](https://wordpress.org/support/article/hardening-wordpress/)
