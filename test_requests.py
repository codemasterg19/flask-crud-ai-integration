import requests
import time
import sys

BASE_URL = "http://localhost:5000"

def print_separator(title):
    print(f"\n{'='*20} {title} {'='*20}")

def wait_for_server():
    print("Esperando a que el servidor inicie...")
    for _ in range(10):
        try:
            requests.get(BASE_URL + "/tasks")
            print("Servidor listo!")
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    print("No se pudo conectar al servidor.")
    return False

def test_create_task():
    print_separator("TEST 1: CREAR TAREA (POST)")
    payload = {
        "title": "Tarea de Prueba",
        "description": "Esto es una prueba automática",
        "priority": "alta",
        "effort_hours": 2.5,
        "status": "pendiente",
        "assigned_to": "Pablo"
    }
    print(f"Enviando POST a {BASE_URL}/tasks con datos:\n{payload}")
    response = requests.post(f"{BASE_URL}/tasks", json=payload)
    print(f"Status Code: {response.status_code}")
    print("Respuesta JSON:", response.json())
    return response.json().get('id')

def test_get_tasks():
    print_separator("TEST 2: OBTENER TODAS (GET)")
    response = requests.get(f"{BASE_URL}/tasks")
    print(f"Status Code: {response.status_code}")
    print("Respuesta JSON:", response.json())

def test_update_task(task_id):
    print_separator(f"TEST 3: ACTUALIZAR TAREA {task_id} (PUT)")
    payload = {
        "title": "Tarea Actualizada",
        "description": "Descripción cambiada",
        "priority": "media",
        "effort_hours": 5.0,
        "status": "en progreso",
        "assigned_to": "Pablo Jimenez"
    }
    print(f"Enviando PUT a {BASE_URL}/tasks/{task_id} con datos:\n{payload}")
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
    print(f"Status Code: {response.status_code}")
    print("Respuesta JSON:", response.json())

def test_delete_task(task_id):
    print_separator(f"TEST 4: ELIMINAR TAREA {task_id} (DELETE)")
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    print(f"Status Code: {response.status_code}")
    print("Respuesta JSON:", response.json())

    # Verificar que ya no existe
    print("Verificando eliminación...")
    check = requests.get(f"{BASE_URL}/tasks/{task_id}")
    print(f"Status Code al intentar leer: {check.status_code} (Esperado 404)")

if __name__ == "__main__":
    if wait_for_server():
        # Limpiar archivo json si es necesario o asumir que empezamos limpios
        # 1. Crear
        task_id = test_create_task()
        if task_id:
            # 2. Leer todas
            test_get_tasks()
            # 3. Actualizar
            test_update_task(task_id)
            # 4. Eliminar
            test_delete_task(task_id)
        else:
            print("Falló la creación de la tarea, no se puede continuar.")
