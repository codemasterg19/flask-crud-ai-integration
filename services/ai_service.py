import os
import re
from openai import AzureOpenAI


class AIService:
    """
    Servicio centralizado para interactuar con Azure OpenAI.
    Maneja generación de descripciones, categorización, estimación y análisis de riesgos.
    """
    
    def __init__(self):
        """Inicializa el cliente de Azure OpenAI leyendo variables de entorno."""
        self.api_key = os.getenv('AZURE_OPENAI_API_KEY')
        self.endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        self.deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
        self.api_version = os.getenv('AZURE_OPENAI_API_VERSION')
        
        # Validar que todas las variables estén configuradas
        if not all([self.api_key, self.endpoint, self.deployment, self.api_version]):
            raise ValueError(
                "Faltan variables de entorno requeridas: "
                "AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, "
                "AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_API_VERSION"
            )
        
        # Inicializar cliente de Azure OpenAI
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.endpoint
        )
    
    def _call_llm(self, prompt: str) -> str:
        """
        Método interno para realizar llamadas al LLM.
        
        Args:
            prompt: El prompt a enviar al modelo
            
        Returns:
            La respuesta del modelo como string
            
        Raises:
            Exception: Si hay error en la llamada al modelo
        """
        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": "Eres un asistente experto en gestión de proyectos y desarrollo de software."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error al llamar a Azure OpenAI: {str(e)}")
    
    def generate_description(self, task: dict) -> str:
        """
        Genera una descripción detallada para una tarea.
        
        Args:
            task: Diccionario con datos de la tarea (title, priority, status, assigned_to)
            
        Returns:
            Descripción generada como texto plano
        """
        prompt = f"""Genera una descripción clara y concisa para la siguiente tarea:

Título: {task.get('title', 'Sin título')}
Prioridad: {task.get('priority', 'Sin prioridad')}
Estado: {task.get('status', 'Sin estado')}
Asignado a: {task.get('assigned_to', 'Sin asignar')}

IMPORTANTE:
- Devuelve SOLO texto plano, sin markdown
- No uses asteriscos, guiones, ni listas
- Máximo 2-3 oraciones
- No incluyas títulos ni encabezados
- Responde directamente con la descripción
"""
        return self._call_llm(prompt)
    
    def categorize_task(self, task: dict) -> str:
        """
        Clasifica una tarea en una categoría específica.
        
        Args:
            task: Diccionario con datos de la tarea
            
        Returns:
            Una de estas categorías: Frontend, Backend, Testing, Infra, DevOps
            
        Raises:
            ValueError: Si la categoría devuelta no es válida
        """
        valid_categories = ['Frontend', 'Backend', 'Testing', 'Infra', 'DevOps']
        
        prompt = f"""Clasifica la siguiente tarea en UNA sola categoría.

Título: {task.get('title', '')}
Descripción: {task.get('description', '')}

Categorías válidas:
- Frontend
- Backend
- Testing
- Infra
- DevOps

IMPORTANTE:
- Responde SOLO con el nombre de la categoría
- No agregues explicaciones ni texto adicional
- Usa exactamente el formato: Frontend, Backend, Testing, Infra o DevOps
"""
        
        category = self._call_llm(prompt).strip()
        
        # Validar que la categoría sea válida
        if category not in valid_categories:
            # Intentar encontrar una categoría válida en la respuesta
            for valid_cat in valid_categories:
                if valid_cat.lower() in category.lower():
                    return valid_cat
            raise ValueError(f"Categoría inválida recibida del LLM: {category}")
        
        return category
    
    def estimate_effort_hours(self, task: dict) -> float:
        """
        Estima el esfuerzo en horas para completar una tarea.
        
        Args:
            task: Diccionario con datos de la tarea (title, description, category)
            
        Returns:
            Estimación de horas como float
            
        Raises:
            ValueError: Si no se puede parsear un número válido de la respuesta
        """
        prompt = f"""Estima el esfuerzo en horas necesario para completar la siguiente tarea:

Título: {task.get('title', '')}
Descripción: {task.get('description', '')}
Categoría: {task.get('category', 'Sin categoría')}

IMPORTANTE:
- Responde SOLO con un número
- Puede ser entero o decimal (ejemplo: 8 o 12.5)
- No agregues palabras como "horas", "aproximadamente", etc.
- Responde únicamente con el valor numérico
"""
        
        response = self._call_llm(prompt)
        
        # Extraer el número de la respuesta usando regex
        # Buscar patrones como: "12", "12.5", "12,5", "aproximadamente 12", etc.
        numbers = re.findall(r'\d+[.,]?\d*', response)
        
        if not numbers:
            raise ValueError(f"No se pudo extraer un número válido de la respuesta: {response}")
        
        # Tomar el primer número encontrado y convertirlo
        try:
            effort_str = numbers[0].replace(',', '.')
            effort = float(effort_str)
            
            if effort < 0:
                raise ValueError("El esfuerzo no puede ser negativo")
            
            return effort
        except (ValueError, IndexError) as e:
            raise ValueError(f"Error al parsear esfuerzo desde '{response}': {str(e)}")
    
    def audit_risks(self, task: dict) -> tuple[str, str]:
        """
        Analiza riesgos de una tarea y genera un plan de mitigación.
        Realiza DOS llamadas separadas al LLM.
        
        Args:
            task: Diccionario con datos de la tarea
            
        Returns:
            Tupla (risk_analysis, risk_mitigation)
        """
        # Primera llamada: Análisis de riesgos
        risk_prompt = f"""Analiza los riesgos potenciales de la siguiente tarea:

Título: {task.get('title', '')}
Descripción: {task.get('description', '')}
Categoría: {task.get('category', 'Sin categoría')}
Prioridad: {task.get('priority', '')}
Esfuerzo estimado: {task.get('effort_hours', 'Sin estimar')} horas

Identifica los principales riesgos técnicos, de recursos o de tiempo.

IMPORTANTE:
- Responde en texto plano, sin markdown
- No uses listas con guiones ni asteriscos
- Máximo 3-4 oraciones
- Se específico y conciso
"""
        
        risk_analysis = self._call_llm(risk_prompt)
        
        # Segunda llamada: Plan de mitigación basado en los riesgos detectados
        mitigation_prompt = f"""Basándote en los siguientes riesgos identificados, genera un plan de mitigación:

TAREA:
Título: {task.get('title', '')}
Descripción: {task.get('description', '')}

RIESGOS IDENTIFICADOS:
{risk_analysis}

Proporciona acciones concretas para mitigar estos riesgos.

IMPORTANTE:
- Responde en texto plano, sin markdown
- No uses listas con guiones ni asteriscos
- Máximo 3-4 oraciones
- Proporciona acciones específicas y prácticas
"""
        
        risk_mitigation = self._call_llm(mitigation_prompt)
        
        return (risk_analysis, risk_mitigation)
