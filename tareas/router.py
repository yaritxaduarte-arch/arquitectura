"""
tasks/router.py
-------------------
Responsabilidad: juntar los routers de las 5 acciones (rebanadas) de
tasks/ en un solo router, para que main.py solo tenga que importar y
registrar una cosa, en vez de las 5 por separado.

Este archivo no tiene lógica propia, solo conecta piezas.
"""

from fastapi import APIRouter

from tareas.crear_tarea import router as crear_tarea_router
from tareas.listar_tareas import router as listar_tareas_router
from tareas.buscar_tarea import router as buscar_tarea_router
from tareas.actualizar_tarea import router as actualizar_tarea_router
from tareas.eliminar_tarea import router as eliminar_tarea_router

router = APIRouter()

router.include_router(crear_tarea_router)
router.include_router(listar_tareas_router)
router.include_router(buscar_tarea_router)
router.include_router(actualizar_tarea_router)
router.include_router(eliminar_tarea_router)