"""
tasks/eliminar_tarea.py
----------------------------
Acción: eliminar una tarea existente.

Responsabilidad: recibir un id, confirmar que la tarea existe, borrarla
de la base de datos. No devuelve contenido (204 No Content), como ya
tenías definido en tu routes.py viejo.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from shared.errores import TaskNotFoundError
from tasks.buscar_tarea import obtener_tarea_o_lanzar_error

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarea(task_id: int, db: Session = Depends(get_db)):
    try:
        tarea = obtener_tarea_o_lanzar_error(db, task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    db.delete(tarea)
    db.commit()