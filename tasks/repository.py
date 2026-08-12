"""
tasks/repository.py
----------------------
Responsabilidad: HABLAR con la base de datos. Solo eso.

Esta capa no sabe nada de HTTP, ni de reglas de negocio. Su único trabajo
es traducir operaciones ("crear", "buscar por id", "listar todas",
"actualizar", "borrar") en consultas de SQLAlchemy contra la tabla `tasks`.

¿Por qué separarlo? Porque si mañana cambian SQLite por PostgreSQL, o por
otra forma de guardar datos, en teoría solo este archivo debería cambiar.
El resto del proyecto (service, controller, routes) no debería enterarse.

Aquí ya está implementado el CRUD básico. Tus compañeros pueden usarlo tal
cual, o extenderlo (por ejemplo, agregar `get_by_title`, o filtros por
`completed`).
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from tasks.model import Task
from tasks.schemas import TaskCreate, TaskUpdate


class TaskRepository:
    """Encapsula todo el acceso a la tabla `tasks`."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, task_data: TaskCreate) -> Task:
        task = Task(**task_data.model_dump())
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_all(self) -> List[Task]:
        return self.db.query(Task).order_by(Task.id).all()

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def update(self, task: Task, task_data: TaskUpdate) -> Task:
        # Solo actualizamos los campos que el cliente realmente envió.
        updates = task_data.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(task, field, value)

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()

    # --- Espacio para que agreguen consultas nuevas ---
    # Ejemplo de algo que podrían necesitar más adelante:
    #
    # def get_by_completed(self, completed: bool) -> List[Task]:
    #     return self.db.query(Task).filter(Task.completed == completed).all()
