"""
tasks/crear_tarea.py
------------------------
Acción: crear una tarea nueva.

Responsabilidad: recibir los datos de una tarea nueva desde HTTP,
validarlos (título no vacío, título no repetido), guardarla en la base
de datos, y devolver la tarea ya creada.

Esta acción está autocontenida: junta lo que antes vivía repartido en
routes.py + controller.py + service.py + repository.py, pero solo para
la operación de "crear".
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional

from database.connection import get_db
from tareas.model import Task
from compartido.esquemas import TaskResponse
from compartido.errores import TituloVacioError, TituloDuplicadoError
from compartido.validaciones import validar_titulo_no_vacio, validar_titulo_no_repetido

router = APIRouter(prefix="/tasks", tags=["Tasks"])


class TaskCreate(BaseModel):
    """Datos que el cliente debe enviar para crear una tarea."""
    title: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=500)
    completed: bool = Field(False)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def crear_tarea(datos: TaskCreate, db: Session = Depends(get_db)):
    try:
        validar_titulo_no_vacio(datos.title)
        validar_titulo_no_repetido(db, datos.title)
    except TituloVacioError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except TituloDuplicadoError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    tarea = Task(**datos.model_dump())
    db.add(tarea)
    db.commit()
    db.refresh(tarea)
    return tarea