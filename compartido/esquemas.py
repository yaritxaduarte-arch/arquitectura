"""
shared/esquemas.py
--------------------
Responsabilidad: definir formas de datos que se comparten entre varias
acciones (rebanadas) de tasks/. Por ahora, solo el esquema de respuesta,
que usan las 5 acciones (crear, listar, consultar, actualizar, eliminar)
para devolver una tarea al cliente.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskResponse(BaseModel):
    """Lo que la API devuelve cuando el cliente consulta una tarea."""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)