# Proyecto Entregable 2 - Integración de IA

API REST con Flask para gestión de tareas con integración de Azure OpenAI.

## 📋 Descripción

Sistema de gestión de tareas que combina un CRUD completo con capacidades de Inteligencia Artificial usando Azure OpenAI. El proyecto mantiene la funcionalidad del Entregable 1 (CRUD básico) y añade 4 nuevos endpoints que utilizan IA para:
- Generar descripciones automáticas
- Categorizar tareas
- Estimar esfuerzo en horas
- Analizar riesgos y planes de mitigación

**Características principales:**
- ✅ Arquitectura por capas (routes, managers, models, services)
- ✅ Persistencia en JSON (sin base de datos)
- ✅ Variables de entorno para credenciales (sin hardcoding)
- ✅ Integración con Azure OpenAI (gpt-4o-mini-entregable2)
- ✅ Validaciones robustas y manejo de errores
- ✅ Parseo inteligente de respuestas del LLM

## 🏗️ Estructura del Proyecto

```
Proyecto-entregable-2-Int/
├── app.py                      # Aplicación principal Flask (incluye load_dotenv)
├── requirements.txt            # Dependencias del proyecto
├── .env.example               # Plantilla de variables de entorno (SIN credenciales)
├── .gitignore                 # Archivos a excluir del repositorio
├── tasks.json                 # Persistencia de tareas en JSON
├── README.md                  # Este archivo
├── test_ai_endpoints.py       # Script de pruebas para endpoints de IA
│
├── models/
│   ├── __init__.py
│   └── task.py               # Modelo Task con campos: id, title, description,
│                             # priority, effort_hours, status, assigned_to,
│                             # category, risk_analysis, risk_mitigation
│
├── managers/
│   ├── __init__.py
│   └── task_manager.py       # Gestor de persistencia en tasks.json
│
├── routes/
│   ├── __init__.py
│   ├── task_routes.py        # Endpoints CRUD (GET, POST, PUT, DELETE)
│   └── ai_task_routes.py     # Endpoints IA (/ai/tasks/*)
│
└── services/
    ├── __init__.py
    └── ai_service.py         # Clase AIService con métodos:
                              # - generate_description()
                              # - categorize_task()
                              # - estimate_effort_hours()
                              # - audit_risks()
```

## ⚙️ Configuración e Instalación

### 1. Clonar o Descargar el Proyecto

```bash
cd Proyecto-entregable-2-Int
```

### 2. Crear Entorno Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Dependencias principales:**
- Flask (framework web)
- openai (SDK de Azure OpenAI)
- python-dotenv (carga de variables de entorno)
- requests (para pruebas HTTP)

### 4. Configurar Variables de Entorno

**PASO CRÍTICO:** Crear archivo `.env` en la raíz del proyecto:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales de Azure OpenAI:

```env
AZURE_OPENAI_API_KEY=tu_api_key_real_aqui
AZURE_OPENAI_ENDPOINT=https://tu-recurso.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini-entregable2
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

⚠️ **IMPORTANTE**: 
- El archivo `.env` contiene credenciales reales y **NO debe incluirse en el ZIP de entrega**
- El archivo `.env.example` es solo una plantilla sin valores sensibles
- Las credenciales se cargan automáticamente al iniciar la aplicación

### 5. Ejecutar el Servidor

```bash
python app.py
```

**Salida esperada:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

El servidor estará disponible en: **http://127.0.0.1:5000**

## 🚀 Endpoints Disponibles

### 📌 CRUD Básico (Entregable 1)

| Método | Endpoint | Descripción | Campos Requeridos |
|--------|----------|-------------|-------------------|
| GET | `/tasks` | Listar todas las tareas | - |
| GET | `/tasks/<id>` | Obtener una tarea específica | - |
| POST | `/tasks` | Crear nueva tarea | title, description, priority, effort_hours, status, assigned_to |
| PUT | `/tasks/<id>` | Actualizar tarea existente | Todos los campos obligatorios |
| DELETE | `/tasks/<id>` | Eliminar tarea | - |

**Valores válidos:**
- `priority`: `baja`, `media`, `alta`, `bloqueante`
- `status`: `pendiente`, `en progreso`, `en revisión`, `completada`

### 🤖 Endpoints de IA (Entregable 2)

| Método | Endpoint | Descripción | Entrada | Salida |
|--------|----------|-------------|---------|--------|
| POST | `/ai/tasks/describe` | Genera descripción automática | title, priority, status, assigned_to | Agrega campo `description` |
| POST | `/ai/tasks/categorize` | Clasifica la tarea | title, description | Agrega campo `category` |
| POST | `/ai/tasks/estimate` | Estima esfuerzo en horas | title, description, category | Agrega campo `effort_hours` (float) |
| POST | `/ai/tasks/audit` | Analiza riesgos (2 llamadas LLM) | title, description, otros campos | Agrega `risk_analysis` y `risk_mitigation` |

**Categorías válidas:** `Frontend`, `Backend`, `Testing`, `Infra`, `DevOps`

## 📝 Ejemplos de Uso con Postman

### ✅ Endpoint 1: POST /ai/tasks/describe

Genera descripción automática usando IA.

**URL:** `http://127.0.0.1:5000/ai/tasks/describe`  
**Method:** POST  
**Headers:** `Content-Type: application/json`

**Request Body:**
```json
{
  "title": "Implementar sistema de autenticación",
  "priority": "alta",
  "status": "pendiente",
  "assigned_to": "María"
}
```

**Response (200 OK):**
```json
{
  "title": "Implementar sistema de autenticación",
  "priority": "alta",
  "status": "pendiente",
  "assigned_to": "María",
  "description": "Desarrollar sistema de autenticación que permita a los usuarios iniciar sesión de forma segura. Incluye validación de credenciales y manejo de sesiones."
}
```

---

### ✅ Endpoint 2: POST /ai/tasks/categorize

Clasifica automáticamente la tarea en una categoría.

**URL:** `http://127.0.0.1:5000/ai/tasks/categorize`  
**Method:** POST

**Request Body:**
```json
{
  "title": "Crear tests unitarios para la API",
  "description": "Implementar suite de pruebas automatizadas"
}
```

**Response (200 OK):**
```json
{
  "title": "Crear tests unitarios para la API",
  "description": "Implementar suite de pruebas automatizadas",
  "category": "Testing"
}
```

**Categorías posibles:** `Frontend`, `Backend`, `Testing`, `Infra`, `DevOps`

---

### ✅ Endpoint 3: POST /ai/tasks/estimate

Estima el esfuerzo en horas (parseado como float).

**URL:** `http://127.0.0.1:5000/ai/tasks/estimate`  
**Method:** POST

**Request Body:**
```json
{
  "title": "Migrar base de datos a PostgreSQL",
  "description": "Migración completa desde MySQL con cero downtime",
  "category": "Backend"
}
```

**Response (200 OK):**
```json
{
  "title": "Migrar base de datos a PostgreSQL",
  "description": "Migración completa desde MySQL con cero downtime",
  "category": "Backend",
  "effort_hours": 24.5
}
```

**Nota:** `effort_hours` es parseado como **float** (no string)

---

### ✅ Endpoint 4: POST /ai/tasks/audit

Analiza riesgos y genera plan de mitigación (2 llamadas al LLM).

**URL:** `http://127.0.0.1:5000/ai/tasks/audit`  
**Method:** POST

**Request Body:**
```json
{
  "title": "Actualizar framework React a v18",
  "description": "Migración de React v16 a v18 en toda la aplicación",
  "category": "Frontend",
  "priority": "alta",
  "effort_hours": 20
}
```

**Response (200 OK):**
```json
{
  "title": "Actualizar framework React a v18",
  "description": "Migración de React v16 a v18 en toda la aplicación",
  "category": "Frontend",
  "priority": "alta",
  "effort_hours": 20,
  "risk_analysis": "Los principales riesgos incluyen incompatibilidades con librerías de terceros, cambios en APIs deprecadas y posibles fallos en componentes existentes durante la migración.",
  "risk_mitigation": "Realizar pruebas exhaustivas en entorno de desarrollo, actualizar dependencias gradualmente, mantener rama de respaldo y documentar todos los cambios de breaking changes antes de desplegar a producción."
}
```

**Nota:** Este endpoint realiza **2 llamadas separadas** al LLM (primero analiza riesgos, luego genera plan de mitigación).

---

## 🧪 Pruebas Automatizadas

El proyecto incluye un script de pruebas para verificar todos los endpoints de IA:

```bash
python test_ai_endpoints.py
```

Este script prueba:
- ✅ Conectividad con el servidor
- ✅ CRUD básico con nuevos campos
- ✅ Los 4 endpoints de IA
- ✅ Parseo correcto de respuestas
- ✅ Manejo de errores

---

## 📊 Modelo de Datos - Task

### Campos Obligatorios (CRUD)
- `id` (string, UUID auto-generado)
- `title` (string)
- `description` (string)
- `priority` (string): `baja`, `media`, `alta`, `bloqueante`
- `effort_hours` (float)
- `status` (string): `pendiente`, `en progreso`, `en revisión`, `completada`
- `assigned_to` (string)

### Campos Opcionales (Entregable 2)
- `category` (string | null): `Frontend`, `Backend`, `Testing`, `Infra`, `DevOps`
- `risk_analysis` (string | null)
- `risk_mitigation` (string | null)

**Ejemplo de tarea completa:**
```json
{
  "id": "f0bd8165-7894-48bd-831e-25e520ddac01",
  "title": "Implementar API REST",
  "description": "Crear endpoints para gestión de usuarios",
  "priority": "alta",
  "effort_hours": 16.5,
  "status": "en progreso",
  "assigned_to": "Carlos",
  "category": "Backend",
  "risk_analysis": "Posibles problemas de rendimiento con alta concurrencia",
  "risk_mitigation": "Implementar caché y optimizar consultas a base de datos"
}
```

---

## ⚠️ Manejo de Errores

La API devuelve códigos HTTP estándar:

| Código | Significado | Ejemplo |
|--------|-------------|---------|
| 200 | OK | Operación exitosa |
| 201 | Created | Tarea creada correctamente |
| 400 | Bad Request | Datos faltantes o inválidos |
| 404 | Not Found | Tarea no encontrada |
| 500 | Internal Server Error | Error en servicio de IA o servidor |

**Ejemplo de error 400:**
```json
{
  "error": "Campos faltantes: title, description"
}
```

**Ejemplo de error 500:**
```json
{
  "error": "Error al generar descripción: Faltan variables de entorno requeridas"
}
```

---

## 📦 Preparar Entrega (ZIP)

### Archivos a INCLUIR en el ZIP:

```
✅ app.py
✅ requirements.txt
✅ .env.example (plantilla sin credenciales)
✅ .gitignore
✅ README.md
✅ test_ai_endpoints.py
✅ models/
✅ managers/
✅ routes/
✅ services/
✅ tasks.json
```

### Archivos a EXCLUIR del ZIP:

```
❌ .env (contiene credenciales reales)
❌ venv/ (entorno virtual completo)
❌ __pycache__/ (archivos compilados de Python)
❌ .agent/ (carpeta de configuración del IDE)
❌ *.pyc (archivos compilados)
```

### Comando para crear ZIP (Windows PowerShell):

```powershell
# Comprimir excluyendo archivos innecesarios
Compress-Archive -Path app.py, requirements.txt, .env.example, .gitignore, README.md, test_ai_endpoints.py, models, managers, routes, services, tasks.json -DestinationPath m2_proyecto_entregable2.zip
```

---

## 🔒 Seguridad y Buenas Prácticas

✅ **Variables de entorno:** Todas las credenciales se leen desde `.env`  
✅ **Sin hardcoding:** No hay API keys en el código fuente  
✅ **.gitignore:** El archivo `.env` está excluido del control de versiones  
✅ **Validaciones:** Todos los endpoints validan datos de entrada  
✅ **Manejo de errores:** Excepciones capturadas y convertidas a HTTP correcto  
✅ **Parseo robusto:** `effort_hours` se extrae correctamente usando regex  
✅ **Arquitectura limpia:** Separación clara de responsabilidades por capas

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.x** - Lenguaje de programación
- **Flask** - Framework web minimalista
- **Azure OpenAI** - Servicio de IA (modelo gpt-4o-mini-entregable2)
- **python-dotenv** - Gestión de variables de entorno
- **JSON** - Persistencia de datos (tasks.json)
- **Requests** - Cliente HTTP para pruebas

---

## ✅ Checklist de Verificación

Antes de entregar, verifica que:

- [ ] El servidor Flask inicia correctamente (`python app.py`)
- [ ] GET `/tasks` devuelve lista de tareas con nuevos campos
- [ ] POST `/ai/tasks/describe` genera descripciones
- [ ] POST `/ai/tasks/categorize` devuelve categoría válida
- [ ] POST `/ai/tasks/estimate` devuelve `effort_hours` como float
- [ ] POST `/ai/tasks/audit` devuelve `risk_analysis` y `risk_mitigation`
- [ ] El archivo `.env` NO está en el ZIP
- [ ] El archivo `.env.example` SÍ está en el ZIP
- [ ] `requirements.txt` está actualizado
- [ ] README.md está completo y actualizado
- [ ] No hay errores de sintaxis (`get_errors` en VS Code)

---

## 📧 Contacto y Soporte

Para dudas o problemas:
1. Verificar que las variables de entorno estén correctamente configuradas
2. Revisar los logs del servidor Flask
3. Consultar la sección de "Manejo de Errores" en este README

---

**Proyecto desarrollado para:** UNIR - Entregable 2  
**Fecha:** Febrero 2026  
**Versión:** 2.0
  "priority": "media",
  "effort_hours": 16
}
```

**Response (200):**
```json
{
  "title": "Actualizar framework a última versión",
  "description": "Actualizar React de v16 a v18",
  "category": "Frontend",
  "priority": "media",
  "effort_hours": 16,
  "risk_analysis": "Los principales riesgos incluyen incompatibilidades con librerías de terceros, cambios en APIs deprecadas y posibles fallos en componentes existentes durante la migración.",
  "risk_mitigation": "Realizar pruebas exhaustivas en entorno de desarrollo, actualizar dependencias gradualmente, mantener rama de respaldo, y documentar todos los cambios de breaking changes antes de desplegar a producción."
}
```
---

**Proyecto desarrollado para:** UNIR - Entregable 2  
**Fecha:** Febrero 2026  
**Versión:** 2.0
