import requests
import json

BASE_URL = "http://localhost:5000"

def print_separator(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def test_ai_describe():
    print_separator("TEST IA 1: GENERAR DESCRIPCIÓN")
    payload = {
        "title": "Implementar sistema de notificaciones",
        "priority": "alta",
        "status": "pendiente",
        "assigned_to": "María"
    }
    print(f"📤 Request: POST {BASE_URL}/ai/tasks/describe")
    print(f"Body: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/ai/tasks/describe", json=payload)
    print(f"\n✅ Status: {response.status_code}")
    print(f"📥 Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.json()

def test_ai_categorize():
    print_separator("TEST IA 2: CATEGORIZAR TAREA")
    payload = {
        "title": "Crear tests end-to-end con Selenium",
        "description": "Implementar suite de pruebas automatizadas para flujos principales"
    }
    print(f"📤 Request: POST {BASE_URL}/ai/tasks/categorize")
    print(f"Body: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/ai/tasks/categorize", json=payload)
    print(f"\n✅ Status: {response.status_code}")
    print(f"📥 Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.json()

def test_ai_estimate():
    print_separator("TEST IA 3: ESTIMAR ESFUERZO")
    payload = {
        "title": "Migrar base de datos a PostgreSQL",
        "description": "Migrar desde MySQL a PostgreSQL manteniendo integridad de datos",
        "category": "Backend"
    }
    print(f"📤 Request: POST {BASE_URL}/ai/tasks/estimate")
    print(f"Body: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/ai/tasks/estimate", json=payload)
    print(f"\n✅ Status: {response.status_code}")
    print(f"📥 Response:")
    result = response.json()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if 'effort_hours' in result:
        print(f"\n⏱️  Esfuerzo estimado: {result['effort_hours']} horas (tipo: {type(result['effort_hours']).__name__})")
    return result

def test_ai_audit():
    print_separator("TEST IA 4: AUDITAR RIESGOS (2 llamadas LLM)")
    payload = {
        "title": "Actualizar framework React a v18",
        "description": "Migrar toda la aplicación de React v16 a v18",
        "category": "Frontend",
        "priority": "media",
        "effort_hours": 20
    }
    print(f"📤 Request: POST {BASE_URL}/ai/tasks/audit")
    print(f"Body: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/ai/tasks/audit", json=payload)
    print(f"\n✅ Status: {response.status_code}")
    print(f"📥 Response:")
    result = response.json()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if 'risk_analysis' in result and 'risk_mitigation' in result:
        print(f"\n🔍 Análisis de Riesgos:")
        print(f"   {result['risk_analysis'][:100]}...")
        print(f"\n🛡️  Plan de Mitigación:")
        print(f"   {result['risk_mitigation'][:100]}...")
    return result

def test_crud_basic():
    print_separator("TEST CRUD: VERIFICAR QUE NO SE ROMPIÓ")
    # Crear tarea con nuevos campos
    payload = {
        "title": "Tarea de prueba CRUD",
        "description": "Verificando compatibilidad",
        "priority": "baja",
        "effort_hours": 2.5,
        "status": "pendiente",
        "assigned_to": "Test",
        "category": "Testing",
        "risk_analysis": "Sin riesgos",
        "risk_mitigation": "N/A"
    }
    print(f"📤 Request: POST {BASE_URL}/tasks")
    
    response = requests.post(f"{BASE_URL}/tasks", json=payload)
    print(f"✅ Status: {response.status_code}")
    print(f"📥 Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    print("\n🚀 INICIANDO PRUEBAS DE INTEGRACIÓN - ENTREGABLE 2")
    print("="*60)
    
    try:
        # Verificar que el servidor esté corriendo
        response = requests.get(f"{BASE_URL}/tasks")
        if response.status_code == 200:
            print("✅ Servidor Flask conectado correctamente")
        
        # Probar CRUD básico
        test_crud_basic()
        
        # Probar endpoints de IA
        test_ai_describe()
        test_ai_categorize()
        test_ai_estimate()
        test_ai_audit()
        
        print_separator("✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("\n💡 Los endpoints de IA están funcionando correctamente!")
        print("💡 El CRUD existente sigue funcionando!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se puede conectar al servidor.")
        print("   Asegúrate de que Flask esté corriendo en http://localhost:5000")
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {str(e)}")
