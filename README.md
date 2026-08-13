
# Gestionar Tareas — Task Manager (CRUD)

Proyecto de la materia **Arquitectura de Software**. CRUD de tareas con
FastAPI + SQLAlchemy + SQLite en el backend, y HTML + CSS + JavaScript
plano en el frontend.

La materia pedía **proponer una arquitectura propia**, no aplicar una ya
existente tal cual. Empezamos con arquitectura por capas
(`model → repository → service → controller → routes`) y la reorganizamos
hacia una propuesta propia inspirada en **Vertical Slice Architecture** +
**Screaming Architecture**: organizar por **acción** en vez de por tipo
técnico, adaptada a nuestro criterio (nombres en español, decisiones
propias sobre qué compartir). El nombre "Vertical Slice" ya existe como
patrón conocido; lo adoptamos como base, no lo inventamos desde cero.

## 🏗️ Arquitectura

```
arquitectura/
├── database/connection.py     # Conexión a SQLite
├── tasks/
│   ├── model.py                  # Tabla en la BD (no es una acción)
│   ├── crear_tarea.py             # Acción: crear
│   ├── listar_tareas.py            # Acción: listar
│   ├── buscar_tarea.py              # Acción: buscar por id
│   ├── actualizar_tarea.py           # Acción: actualizar
│   ├── eliminar_tarea.py              # Acción: eliminar
│   └── router.py                       # Junta las 5 en un solo router
├── shared/
│   ├── esquemas.py                # Forma de una tarea en las respuestas
│   ├── errores.py                   # Errores de negocio compartidos
│   └── validaciones.py               # Título no vacío / no repetido
├── frontend/tasks/                # HTML + CSS + JS de la interfaz
├── tests/test_tasks.py           # Pruebas contra los endpoints HTTP
├── main.py                       # Registra rutas y sirve el frontend
└── requirements.txt
```

Cada acción es un archivo autocontenido: su ruta HTTP, su validación y su
acceso a la base de datos, todo junto. Antes, entender "crear una tarea"
significaba abrir 4 archivos distintos; ahora es solo
`tasks/crear_tarea.py`. Lo que se repite entre acciones (validaciones,
formato de respuesta, errores) vive en `shared/`, para no duplicar código.

## 🖥️ Frontend

HTML + CSS + JS plano, servido por FastAPI con `StaticFiles`, conectado a
la API con `fetch()`. `index.html` lista y filtra tareas; `formulario.html`
sirve tanto para crear como para editar (con navegación real entre
páginas, sin modal).

## 🚀 Cómo correrlo

```bash
python -m venv venv
venv\Scripts\activate          # Windows
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

Abrir `http://127.0.0.1:8000` para la app, o `http://127.0.0.1:8000/docs`
para la documentación interactiva (Swagger).

## 🧪 Pruebas

```bash
pytest -v
```

Hablan directo con los endpoints HTTP, así que no les importa cómo está
organizado el código por dentro.

## 📌 Endpoints

| Método | Ruta          | Acción responsable           |
|--------|---------------|-------------------------------|
| POST   | `/tasks`      | `tasks/crear_tarea.py`        |
| GET    | `/tasks`      | `tasks/listar_tareas.py`      |
| GET    | `/tasks/{id}` | `tasks/buscar_tarea.py`       |
| PUT    | `/tasks/{id}` | `tasks/actualizar_tarea.py`   |
| DELETE | `/tasks/{id}` | `tasks/eliminar_tarea.py`     |

## ✅ Reglas de negocio

- El título no puede estar vacío ni ser solo espacios.
- No puede haber dos tareas con el mismo título.

Ambas viven en `shared/validaciones.py` y se usan al crear y al
actualizar.

## 👥 Para el equipo

- **Acción nueva** → archivo nuevo en `tasks/`, registrarlo en `router.py`.
- **Algo que se repite entre acciones** → `shared/`.
- **Campo nuevo en la tabla** → empezar por `tasks/model.py`.
- **Prueba nueva** → `tests/test_tasks.py`.

## ✅ Estado

- [x] Backend por acción (Vertical Slice)
- [x] Validaciones: título no vacío, no repetido
- [x] Frontend conectado vía `fetch()`
- [x] CRUD probado end-to-end (navegador + pytest)
- [ ] Reglas de negocio adicionales (equipo)
- [ ] Autenticación / usuarios (si el proyecto crece)
```