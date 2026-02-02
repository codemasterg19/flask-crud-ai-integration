- Quiero crear una API REST con Flask para gestionar tareas asignadas a usuarios.
- El proyecto debe estar organizado con arquitectura por capas (routes, managers, models) y ser escalable para siguientes módulos.
- Los datos se guardarán y leerán desde un archivo **tasks.json** (no usar base de datos en este entregable).
- La API debe devolver siempre respuestas en formato **JSON**.

- La entidad **Task** tendrá estos campos:
  - id (primary key)
  - title (título)
  - description (texto largo)
  - priority (baja, media, alta, bloqueante)
  - effort_hours (número decimal)
  - status (pendiente, en progreso, en revisión, completada)
  - assigned_to (string, persona asignada)

- Endpoints requeridos:
  - Crear una tarea (POST /tasks)
  - Leer todas las tareas (GET /tasks)
  - Leer una tarea específica (GET /tasks/<id>)
  - Actualizar una tarea (PUT /tasks/<id>)
  - Eliminar una tarea (DELETE /tasks/<id>)

- Debes crear:
  - La arquitectura completa de ficheros del proyecto.
  - El entorno virtual e instalación de librerías necesarias.
  - El archivo **requirements.txt**.
  - Un fichero de rutas donde se registren todas las rutas y llamen a la lógica.

- Clases requeridas:
  - **Clase Task**
    - to_dict(): convierte el objeto a diccionario
    - from_dict(): crea un Task desde un diccionario
  - **Clase TaskManager** (métodos estáticos)
    - load_tasks(): carga tareas desde tasks.json y las convierte en objetos Task
    - save_tasks(): guarda lista de Task en tasks.json

- Hazlo paso a paso para que yo vaya viendo cómo lo haces.
- paso 1: Crear el entorno virtual y activarlo
- paso 2: Instalar dependencias
- paso 3: Crear requirements.txt
- paso 4: Crear la arquitectura de carpetas y el archivo tasks.json inicial
- paso 5: Crear app.py como punto de entrada (inicializa Flask y registra rutas)
- paso 6: Crear models/task.py con la clase Task
- paso 7: Crear managers/task_manager.py con TaskManager (leer/guardar JSON)
- paso 8: Crear routes/task_routes.py con los endpoints REST requeridos
- paso 9: Probar endpoints con ejemplos (curl o Postman) y mostrar respuestas JSON esperadas

- Entrega final:
  - Generar un ZIP con nombre: **m2_proyecto_nombre_apellido.zip**
  - No incluir la carpeta del entorno virtual dentro del zip
