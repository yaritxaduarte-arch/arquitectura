"""
tasks/routes.py
------------------
Responsabilidad: definir los endpoints HTTP de tareas y conectarlos con
el controller.

Este archivo solo define "rutas": qué URL, qué verbo HTTP, qué status code
devuelve, y qué controller la atiende. No tiene lógica propia.
"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.connection import get_db
from tasks.controller import TaskController
from tasks.schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_controller(db: Session = Depends(get_db)) -> TaskController:
    return TaskController(db)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, controller: TaskController = Depends(get_controller)):
    return controller.create_task(task_data)


@router.get("", response_model=List[TaskResponse])
def list_tasks(controller: TaskController = Depends(get_controller)):
    return controller.list_tasks()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, controller: TaskController = Depends(get_controller)):
    return controller.get_task(task_id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, controller: TaskController = Depends(get_controller)):
    return controller.update_task(task_id, task_data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, controller: TaskController = Depends(get_controller)):
    controller.delete_task(task_id)
