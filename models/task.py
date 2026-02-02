import uuid

class Task:
    """
    Representa una tarea en el sistema.
    """
    def __init__(self, title, description, priority, effort_hours, status, assigned_to, 
                 id=None, category=None, risk_analysis=None, risk_mitigation=None):
        # Generar ID único si no viene informado
        self.id = id if id else str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.effort_hours = float(effort_hours)
        self.status = status
        self.assigned_to = assigned_to
        # Nuevos campos para Entregable 2
        self.category = category
        self.risk_analysis = risk_analysis
        self.risk_mitigation = risk_mitigation

    def to_dict(self):
        """Convierte el objeto Task a un diccionario."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "effort_hours": self.effort_hours,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "category": self.category,
            "risk_analysis": self.risk_analysis,
            "risk_mitigation": self.risk_mitigation
        }

    @staticmethod
    def from_dict(data):
        """Crea una instancia de Task desde un diccionario."""
        return Task(
            id=data.get("id"),
            title=data.get("title"),
            description=data.get("description"),
            priority=data.get("priority"),
            effort_hours=data.get("effort_hours"),
            status=data.get("status"),
            assigned_to=data.get("assigned_to"),
            category=data.get("category"),
            risk_analysis=data.get("risk_analysis"),
            risk_mitigation=data.get("risk_mitigation")
        )
