"""
tasks/model.py
----------------
Responsabilidad: definir cómo se ve una tarea EN LA BASE DE DATOS.

Esto es el modelo de SQLAlchemy (ORM), es decir, el mapeo entre la tabla
"tasks" en SQLite y una clase de Python. No confundir con schemas.py, que
define cómo se ve una tarea en la API (JSON de entrada/salida).

Si tus compañeros necesitan agregar un campo nuevo a las tareas (por ejemplo
"prioridad" o "fecha límite"), este es el archivo que deben tocar primero.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from database.connection import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False)
    description = Column(String(500), nullable=True)
    completed = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<Task id={self.id} title={self.title!r} completed={self.completed}>"
