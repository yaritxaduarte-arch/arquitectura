"""
tasks/schemas.py
------------------
Responsabilidad: definir cómo se ve una tarea EN LA API (lo que entra y
sale como JSON). Esto son schemas de Pydantic, no modelos de base de datos.

- TaskCreate  -> lo que el cliente envía para crear una tarea (POST /tasks)
- TaskUpdate  -> lo que el cliente envía para actualizar una tarea (PUT /tasks/{id})
- TaskResponse -> lo que la API devuelve al cliente

Separar esto del modelo (tasks/model.py) es justamente lo que nos permite,
por ejemplo, no exponer campos internos, o pedir datos distintos a los que
se guardan.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=120, description="Título de la tarea")
    description: Optional[str] = Field(None, max_length=500, description="Detalle opcional")
    completed: bool = Field(False, description="Si la tarea ya está completada")


class TaskCreate(TaskBase):
    """Datos necesarios para crear una tarea nueva."""
    pass


class TaskUpdate(BaseModel):
    """
    Datos para actualizar una tarea existente.
    Todos los campos son opcionales: el cliente solo manda lo que quiere cambiar.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """Lo que la API devuelve cuando consultas una tarea."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)  # permite construir esto directo desde el modelo SQLAlchemy
