# Utilidades compartidas entre módulos

def format_response(data, success=True, message=None):
    """Formatea respuestas estándar de la API"""
    return {
        "success": success,
        "data": data,
        "message": message
    }

def validate_content(content):
    """Valida que el contenido generado tenga el formato correcto"""
    if not content or len(content) < 50:
        return False
    return True
