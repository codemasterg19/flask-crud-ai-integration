---
trigger: always_on
---

# Reglas del agente — Proyecto Flask Gestión de Tareas

## Reglas generales
- Seguir estrictamente las instrucciones definidas en `instrucciones.md`.
- No agregar funcionalidades que no estén explícitamente solicitadas.
- No adelantar pasos futuros si no han sido solicitados.
- Priorizar claridad y simplicidad sobre complejidad innecesaria.

---

## Reglas de arquitectura
- Mantener separación estricta por capas:
  - routes → solo definición de endpoints
  - managers → lógica de negocio y persistencia
  - models → definición de entidades
- Prohibido colocar lógica de negocio dentro de rutas Flask.
- No usar bases de datos (SQL, NoSQL, ORM, SQLAlchemy, etc.).
- Persistencia únicamente mediante el archivo `tasks.json`.

---

## Reglas sobre Flask y API
- Usar Flask como único framework backend.
- Implementar endpoints REST con métodos HTTP correctos.
- Devolver SIEMPRE respuestas en formato JSON.
- Incluir códigos HTTP adecuados:
  - 200 OK
  - 201 Created
  - 400 Bad Request
  - 404 Not Found

---

## Reglas de datos
- Validar datos de entrada en POST y PUT.
- Campos obligatorios: title, description, priority, effort_hours, status, assigned_to.
- `priority` solo puede ser: baja, media, alta, bloqueante.
- `status` solo puede ser: pendiente, en progreso, en revisión, completada.
- `effort_hours` debe ser un número decimal positivo.
- El campo `id` debe generarse automáticamente si no se proporciona.

---

## Reglas de persistencia JSON
- `TaskManager` es la única clase autorizada para leer o escribir `tasks.json`.
- Si `tasks.json` no existe, debe crearse automáticamente.
- Si el archivo está vacío, debe interpretarse como lista vacía.
- Manejar errores de lectura/escritura con mensajes claros.

---

## Reglas de código
- Código modular, legible y comentado.
- Nombres de funciones y variables descriptivos.
- No duplicar lógica.
- No usar prints para debug en la versión final.
- Usar funciones pequeñas y claras.

---

## Reglas de entrega
- No incluir la carpeta del entorno virtual (`venv`) en la entrega final.
- Incluir `requirements.txt`.
- El proyecto debe poder ejecutarse con:
  `pip install -r requirements.txt`
  `python app.py`
