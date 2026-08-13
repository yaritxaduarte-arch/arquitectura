"""
tasks/buscar_tarea.py
--------------------------
Acción: buscar una tarea puntual por su id.

Responsabilidad: recibir un id desde la URL, buscar esa tarea en la base
de datos, y devolverla. Si no existe, responder con un 404.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from tareas.model import Task
from compartido.esquemas import TaskResponse
from compartido.errores import TaskNotFoundError

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def obtener_tarea_o_lanzar_error(db: Session, task_id: int) -> Task:
    """
    Busca una tarea por id. Si no existe, lanza TaskNotFoundError.

    Esta función la van a reutilizar también actualizar_tarea.py y
    eliminar_tarea.py, ya que las tres necesitan primero confirmar que
    la tarea existe antes de hacer su trabajo.
    """
    tarea = db.query(Task).filter(Task.id == task_id).first()
    if tarea is None:
        raise TaskNotFoundError(f"No existe una tarea con id={task_id}")
    return tarea


@router.get("/{task_id}", response_model=TaskResponse)
def buscar_tarea(task_id: int, db: Session = Depends(get_db)):
    try:
        return obtener_tarea_o_lanzar_error(db, task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))