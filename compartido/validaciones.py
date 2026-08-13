"""
shared/validaciones.py
--------------------------
Responsabilidad: reglas de negocio que se comparten entre varias acciones
(rebanadas) de tasks/. Por ahora, las dos validaciones sobre el título
de una tarea: que no esté vacío y que no se repita.

Estas funciones no devuelven nada si todo está bien; si algo está mal,
lanzan uno de los errores definidos en shared/errores.py. Quien llama a
estas funciones es responsable de capturar ese error y convertirlo en
una respuesta HTTP adecuada (eso pasa en cada archivo de acción).
"""

from typing import Optional

from sqlalchemy.orm import Session

from tareas.model import Task
from compartido.errores import TituloVacioError, TituloDuplicadoError


def validar_titulo_no_vacio(titulo: str) -> None:
    """Lanza TituloVacioError si el título está vacío o son solo espacios."""
    if not titulo or not titulo.strip():
        raise TituloVacioError("El título de la tarea no puede estar vacío.")


def validar_titulo_no_repetido(db: Session, titulo: str, task_id: Optional[int] = None) -> None:
    """
    Lanza TituloDuplicadoError si ya existe otra tarea con ese mismo título.

    task_id: al actualizar una tarea, se le pasa su propio id para que la
    validación no la compare consigo misma (si no, editar una tarea sin
    cambiar el título siempre fallaría, porque "chocaría" con ella misma).
    """
    query = db.query(Task).filter(Task.title == titulo)
    if task_id is not None:
        query = query.filter(Task.id != task_id)

    if query.first() is not None:
        raise TituloDuplicadoError(f"Ya existe una tarea con el título '{titulo}'.")