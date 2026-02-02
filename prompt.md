Rol:

Actúa como un Agente Experto en Python y Flask (API REST) + Integración de LLMs, con dominio en:
Flask, routing, blueprints, arquitectura por capas, validación de datos, manejo de JSON en archivos, buenas prácticas de ingeniería, e integración con SDKs de IA (OpenAI / Azure OpenAI) incluyendo prompt engineering y parsing de salidas.

Contexto:

Debes seguir estrictamente las instrucciones del Entregable 2: Integración de endpoints de IA, partiendo del proyecto del Entregable 1 (CRUD Task con persistencia en tasks.json, sin base de datos). 

entregable2

Objetivo:

Mantener el CRUD existente y agregar:

Nuevos campos a Task: category, risk_analysis, risk_mitigation

Nuevos endpoints IA:

POST /ai/tasks/describe

POST /ai/tasks/categorize

POST /ai/tasks/estimate

POST /ai/tasks/audit (2 llamadas al LLM)

Restricciones obligatorias:

No usar base de datos. Persistencia SOLO en tasks.json.

No incluir credenciales en el código ni en el ZIP.

Usar variables de entorno para API key y endpoint.

Mantener arquitectura por capas:

routes/ para endpoints

managers/ para JSON CRUD (ya existente)

models/ para Task

services/ para lógica de IA (nuevo)

Respuestas en JSON con HTTP correcto: 200, 201, 400, 404, 500.

En /ai/tasks/estimate el campo effort_hours debe ser float (parsear salida del LLM).

En /ai/tasks/audit se deben hacer dos peticiones al LLM: riesgos y mitigación.

Tu output:
Entregar por bloques:

Análisis del documento + requisitos de endpoints

Plan paso a paso de implementación sobre el proyecto existente

Estructura final de carpetas

Código completo por archivo (solo los cambios y los nuevos archivos, sin duplicar lo que ya existe si no cambia)

requirements.txt actualizado

Cómo ejecutar

Cómo probar con Postman/curl (ejemplos por endpoint y responses esperadas)