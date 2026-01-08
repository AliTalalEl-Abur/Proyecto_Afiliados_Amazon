"""
Script de prueba simple para el backend
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Prueba el endpoint de health"""
    print("🔍 Probando /health...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_root():
    """Prueba el endpoint raíz"""
    print("🔍 Probando /...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_generate_article():
    """Prueba el endpoint de generación (con datos de ejemplo)"""
    print("🔍 Probando /generate_article...")
    print("⚠️  NOTA: Este test fallará sin un PDF real")
    
    payload = {
        "pdf_url": "https://example.com/manual.pdf",
        "error": "Error E03 - Fallo de comunicación",
        "model": "Amazon Echo Dot 4"
    }
    
    print(f"Request: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate_article",
            json=payload,
            timeout=60
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
    
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 TEST DEL BACKEND - FASE 1")
    print("=" * 50)
    print()
    
    try:
        test_root()
        test_health()
        
        # Descomentar cuando tengas un PDF real:
        # test_generate_article()
        
        print("✅ Tests básicos completados")
        print()
        print("📝 Para probar la generación de artículos:")
        print("   1. Consigue un PDF de manual técnico")
        print("   2. Súbelo a un servidor o usa URL pública")
        print("   3. Descomenta test_generate_article() arriba")
        print("   4. Ejecuta este script de nuevo")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("   Asegúrate de que el servidor esté ejecutándose:")
        print("   python main.py")
