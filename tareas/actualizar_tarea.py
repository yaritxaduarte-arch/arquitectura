"""
tasks/actualizar_tarea.py
------------------------------
Acción: actualizar una tarea existente.

Responsabilidad: recibir un id y los campos a cambiar, confirmar que la
tarea existe, validar el título si viene incluido (que no esté vacío y
que no choque con el de otra tarea), aplicar los cambios y devolver la
tarea actualizada.

El cliente puede mandar solo los campos que quiere cambiar (por ejemplo,
solo `completed`, sin tocar el título) — por eso todos los campos del
esquema de entrada son opcionales.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from database.connection import get_db
from compartido.esquemas import TaskResponse
from compartido.errores import TaskNotFoundError, TituloVacioError, TituloDuplicadoError
from compartido.validaciones import validar_titulo_no_vacio, validar_titulo_no_repetido
from tareas.buscar_tarea import obtener_tarea_o_lanzar_error

router = APIRouter(prefix="/tasks", tags=["Tasks"])


class TaskUpdate(BaseModel):
    """Datos que el cliente puede enviar para actualizar una tarea.
    Todos los campos son opcionales: solo se cambia lo que se envía."""
    title: Optional[str] = Field(None, min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None


@router.put("/{task_id}", response_model=TaskResponse)
def actualizar_tarea(task_id: int, datos: TaskUpdate, db: Session = Depends(get_db)):
    try:
        tarea = obtener_tarea_o_lanzar_error(db, task_id)

        if datos.title is not None:
            validar_titulo_no_vacio(datos.title)
            validar_titulo_no_repetido(db, datos.title, task_id=task_id)

    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TituloVacioError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except TituloDuplicadoError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(tarea, campo, valor)

    db.commit()
    db.refresh(tarea)
    return tarea