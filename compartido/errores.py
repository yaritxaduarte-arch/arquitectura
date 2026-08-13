"""
shared/errores.py
--------------------
Responsabilidad: definir errores de negocio que se comparten entre varias
acciones (rebanadas) de tasks/.

Estos NO son errores de HTTP (eso lo decide cada acción al capturarlos),
son errores internos de la aplicación que describen qué salió mal en
términos del negocio, no del protocolo web.
"""


class TaskNotFoundError(Exception):
    """Se lanza cuando se busca una tarea que no existe."""
    pass


class TituloDuplicadoError(Exception):
    """Se lanza cuando se intenta crear o renombrar una tarea con un
    título que ya existe en otra tarea."""
    pass


class TituloVacioError(Exception):
    """Se lanza cuando el título de una tarea está vacío o son solo
    espacios en blanco."""
    pass