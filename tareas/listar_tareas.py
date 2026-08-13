"""
tasks/listar_tareas.py
---------------------------
Acción: listar todas las tareas.

Responsabilidad: consultar todas las tareas guardadas en la base de datos
y devolverlas. Es la acción más simple: no recibe datos del cliente y no
tiene reglas de negocio que validar.
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from tareas.model import Task
from compartido.esquemas import TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=List[TaskResponse])
def listar_tareas(db: Session = Depends(get_db)):
    return db.query(Task).order_by(Task.id).all()