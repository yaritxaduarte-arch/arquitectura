"""
tasks/controller.py
----------------------
Responsabilidad: hacer de puente entre HTTP (FastAPI) y las reglas de
negocio (service.py).

El controller:
- Recibe los datos ya validados por Pydantic (schemas.py).
- Llama al service correspondiente.
- Traduce los errores de negocio (como TaskNotFoundError) en respuestas
  HTTP con el código de estado correcto (404, etc).
- Convierte el modelo de base de datos en el schema de respuesta.

Este archivo NO contiene reglas de negocio (eso va en service.py) y NO
contiene queries de SQL (eso va en repository.py). Solo coordina.
"""

from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from tasks.schemas import TaskCreate, TaskUpdate, TaskResponse
from tasks.service import TaskService, TaskNotFoundError


class TaskController:
    def __init__(self, db: Session):
        self.service = TaskService(db)

    def create_task(self, task_data: TaskCreate) -> TaskResponse:
        task = self.service.create_task(task_data)
        return TaskResponse.model_validate(task)

    def list_tasks(self) -> List[TaskResponse]:
        tasks = self.service.list_tasks()
        return [TaskResponse.model_validate(t) for t in tasks]

    def get_task(self, task_id: int) -> TaskResponse:
        try:
            task = self.service.get_task(task_id)
        except TaskNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        return TaskResponse.model_validate(task)

    def update_task(self, task_id: int, task_data: TaskUpdate) -> TaskResponse:
        try:
            task = self.service.update_task(task_id, task_data)
        except TaskNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        return TaskResponse.model_validate(task)

    def delete_task(self, task_id: int) -> None:
        try:
            self.service.delete_task(task_id)
        except TaskNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
