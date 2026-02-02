import json
import os
from models.task import Task

TASKS_FILE = 'tasks.json'

class TaskManager:
    """
    Gestor de persistencia para las tareas.
    Se encarga de leer y escribir en el archivo JSON.
    """

    @staticmethod
    def load_tasks():
        """
        Lee las tareas desde tasks.json y devuelve una lista de objetos Task.
        Si el archivo no existe o está vacío, devuelve una lista vacía.
        """
        if not os.path.exists(TASKS_FILE):
            return []

        try:
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                return [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al leer tasks.json: {e}")
            return []

    @staticmethod
    def save_tasks(tasks):
        """
        Recibe una lista de objetos Task y la guarda en tasks.json.
        """
        try:
            data = [task.to_dict() for task in tasks]
            with open(TASKS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error al guardar tasks.json: {e}")
