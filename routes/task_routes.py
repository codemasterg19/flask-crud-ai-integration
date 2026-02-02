from flask import Blueprint, request, jsonify
from models.task import Task
from managers.task_manager import TaskManager

task_bp = Blueprint('task_bp', __name__)

# Validadores
VALID_PRIORITIES = ['baja', 'media', 'alta', 'bloqueante']
VALID_STATUSES = ['pendiente', 'en progreso', 'en revisión', 'completada']

def validate_task_data(data):
    """Valida los datos de entrada para crear o actualizar una tarea."""
    errors = []
    required_fields = ['title', 'description', 'priority', 'effort_hours', 'status', 'assigned_to']
    
    # 1. Validar campos obligatorios
    for field in required_fields:
        if field not in data or data[field] is None:
            errors.append(f"El campo '{field}' es obligatorio.")
            
    # Si faltan campos, retornamos errores básicos antes de validar contenido
    if errors:
        return errors

    # 2. Validar contenido de campos
    if data.get('priority') not in VALID_PRIORITIES:
        errors.append(f"Prioridad inválida. Valores permitidos: {', '.join(VALID_PRIORITIES)}")
        
    if data.get('status') not in VALID_STATUSES:
        errors.append(f"Estado inválido. Valores permitidos: {', '.join(VALID_STATUSES)}")
        
    try:
        effort = float(data.get('effort_hours'))
        if effort < 0:
            errors.append("effort_hours debe ser un número positivo.")
    except (ValueError, TypeError):
        errors.append("effort_hours debe ser un número válido.")

    return errors

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = TaskManager.load_tasks()
    return jsonify([task.to_dict() for task in tasks]), 200

@task_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    tasks = TaskManager.load_tasks()
    task = next((t for t in tasks if t.id == task_id), None)
    if task:
        return jsonify(task.to_dict()), 200
    return jsonify({"error": "Tarea no encontrada"}), 404

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Cuerpo de la petición vacío o JSON inválido"}), 400
    
    errors = validate_task_data(data)
    if errors:
        return jsonify({"errors": errors}), 400
        
    new_task = Task(
        title=data['title'],
        description=data['description'],
        priority=data['priority'],
        effort_hours=data['effort_hours'],
        status=data['status'],
        assigned_to=data['assigned_to'],
        category=data.get('category'),
        risk_analysis=data.get('risk_analysis'),
        risk_mitigation=data.get('risk_mitigation')
    )
    
    tasks = TaskManager.load_tasks()
    tasks.append(new_task)
    TaskManager.save_tasks(tasks)
    
    return jsonify(new_task.to_dict()), 201

@task_bp.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Cuerpo de la petición vacío o JSON inválido"}), 400

    tasks = TaskManager.load_tasks()
    task = next((t for t in tasks if t.id == task_id), None)
    
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
        
    # Validación completa de datos
    errors = validate_task_data(data)
    if errors:
        return jsonify({"errors": errors}), 400

    # Actualizar campos obligatorios
    task.title = data['title']
    task.description = data['description']
    task.priority = data['priority']
    task.effort_hours = float(data['effort_hours'])
    task.status = data['status']
    task.assigned_to = data['assigned_to']
    
    # Actualizar campos opcionales (Entregable 2)
    if 'category' in data:
        task.category = data['category']
    if 'risk_analysis' in data:
        task.risk_analysis = data['risk_analysis']
    if 'risk_mitigation' in data:
        task.risk_mitigation = data['risk_mitigation']
    
    TaskManager.save_tasks(tasks)
    return jsonify(task.to_dict()), 200

@task_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = TaskManager.load_tasks()
    task = next((t for t in tasks if t.id == task_id), None)
    
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
        
    tasks.remove(task)
    TaskManager.save_tasks(tasks)
    return jsonify({"message": "Tarea eliminada correctamente"}), 200
