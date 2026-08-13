"""
main.py
---------
Punto de entrada de la aplicación.

Responsabilidad: crear la app de FastAPI, crear las tablas en la base de
datos (si no existen) y registrar las rutas de cada feature.

Cuando el proyecto crezca y agreguen otra feature (por ejemplo `users/`),
este es el único archivo donde deben "engancharla":

    from users.routes import router as users_router
    app.include_router(users_router)
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database.connection import Base, engine
from tasks.router import router as tasks_router

# Crea las tablas definidas en los modelos (tasks/model.py) si no existen aún.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gestionar Tareas API",
    description="CRUD de tareas construido con Screaming Architecture.",
    version="0.1.0",
)

app.include_router(tasks_router)

app.mount("/", StaticFiles(directory="frontend/tasks", html=True), name="frontend")