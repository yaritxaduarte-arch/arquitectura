"""
tasks/service.py
-------------------
Responsabilidad: REGLAS DE NEGOCIO.

Esta es, casi siempre, la capa donde tus compañeros van a querer meter
lógica adicional. El service NO habla directamente con la base de datos
(eso ya lo hace repository.py) y NO sabe nada de HTTP (eso lo maneja
controller.py). Su trabajo es decidir SI algo se puede hacer, y aplicar
validaciones o reglas que no son responsabilidad de la base de datos.

Ejemplos de reglas de negocio que podrían agregar aquí:
- No permitir crear una tarea con un título duplicado.
- No permitir marcar como completada una tarea que ya estaba completada.
- Registrar un log cada vez que se elimina una tarea.
- Limitar cuántas tareas puede tener un usuario.

Por ahora, esta capa hace lo mínimo (delegar al repository) y deja
marcado con TODO dónde se pueden agregar esas reglas.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from tasks.model import Task
from tasks.repository import TaskRepository
from tasks.schemas import TaskCreate, TaskUpdate


class TaskNotFoundError(Exception):
    """Se lanza cuando se busca una tarea que no existe."""
    pass


class TaskService:
    def __init__(self, db: Session):
        self.repository = TaskRepository(db)

    def create_task(self, task_data: TaskCreate) -> Task:
        # TODO (equipo): aquí podrían validar, por ejemplo, que no exista
        # ya una tarea con el mismo título antes de crearla.
        return self.repository.create(task_data)

    def list_tasks(self) -> List[Task]:
        # TODO (equipo): aquí podrían agregar filtros, por ejemplo
        # list_tasks(completed: Optional[bool] = None)
        return self.repository.get_all()

    def get_task(self, task_id: int) -> Task:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"No existe una tarea con id={task_id}")
        return task

    def update_task(self, task_id: int, task_data: TaskUpdate) -> Task:
        task = self.get_task(task_id)  # lanza TaskNotFoundError si no existe
        # TODO (equipo): aquí podrían agregar reglas, por ejemplo no dejar
        # "reabrir" una tarea completada, o validar transiciones de estado.
        return self.repository.update(task, task_data)

    def delete_task(self, task_id: int) -> None:
        task = self.get_task(task_id)  # lanza TaskNotFoundError si no existe
        # TODO (equipo): aquí podrían agregar, por ejemplo, un log de auditoría.
        self.repository.delete(task)
