from flask import Blueprint, request, jsonify
from services.ai_service import AIService

ai_task_bp = Blueprint('ai_task_bp', __name__, url_prefix='/ai/tasks')

# Instancia del servicio de IA
ai_service = AIService()


@ai_task_bp.route('/describe', methods=['POST'])
def describe_task():
    """
    Genera una descripción para una tarea usando IA.
    
    Entrada: Tarea con description vacía o ausente
    Salida: La misma tarea con description generada por IA
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Cuerpo de la petición vacío o JSON inválido"}), 400
        
        # Validar campos mínimos necesarios
        required_fields = ['title', 'priority', 'status', 'assigned_to']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Campos faltantes: {', '.join(missing_fields)}"}), 400
        
        # Generar descripción usando IA
        generated_description = ai_service.generate_description(data)
        
        # Actualizar la tarea con la descripción generada
        data['description'] = generated_description
        
        return jsonify(data), 200
        
    except Exception as e:
        return jsonify({"error": f"Error al generar descripción: {str(e)}"}), 500


@ai_task_bp.route('/categorize', methods=['POST'])
def categorize_task():
    """
    Clasifica una tarea en una categoría usando IA.
    
    Entrada: Tarea sin category
    Salida: La misma tarea con category asignada
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Cuerpo de la petición vacío o JSON inválido"}), 400
        
        # Validar que tenga al menos title
        if 'title' not in data:
            return jsonify({"error": "El campo 'title' es obligatorio"}), 400
        
        # Categorizar tarea usando IA
        category = ai_service.categorize_task(data)
        
        # Actualizar la tarea con la categoría
        data['category'] = category
        
        return jsonify(data), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error al categorizar tarea: {str(e)}"}), 500


@ai_task_bp.route('/estimate', methods=['POST'])
def estimate_task():
    """
    Estima el esfuerzo en horas para una tarea usando IA.
    
    Entrada: Tarea sin effort_hours
    Salida: La misma tarea con effort_hours estimado (float)
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Cuerpo de la petición vacío o JSON inválido"}), 400
        
        # Validar campos mínimos
        required_fields = ['title', 'description']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Campos faltantes: {', '.join(missing_fields)}"}), 400
        
        # Estimar esfuerzo usando IA
        effort_hours = ai_service.estimate_effort_hours(data)
        
        # Actualizar la tarea con el esfuerzo estimado (como float)
        data['effort_hours'] = effort_hours
        
        return jsonify(data), 200
        
    except ValueError as e:
        return jsonify({"error": f"Error al parsear esfuerzo: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error al estimar esfuerzo: {str(e)}"}), 500


@ai_task_bp.route('/audit', methods=['POST'])
def audit_task():
    """
    Analiza riesgos y genera plan de mitigación para una tarea usando IA.
    Realiza DOS llamadas al LLM.
    
    Entrada: Tarea sin risk_analysis y risk_mitigation
    Salida: La misma tarea con ambos campos completados
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Cuerpo de la petición vacío o JSON inválido"}), 400
        
        # Validar campos mínimos
        required_fields = ['title', 'description']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Campos faltantes: {', '.join(missing_fields)}"}), 400
        
        # Realizar auditoría de riesgos (2 llamadas al LLM)
        risk_analysis, risk_mitigation = ai_service.audit_risks(data)
        
        # Actualizar la tarea con el análisis
        data['risk_analysis'] = risk_analysis
        data['risk_mitigation'] = risk_mitigation
        
        return jsonify(data), 200
        
    except Exception as e:
        return jsonify({"error": f"Error al auditar tarea: {str(e)}"}), 500
