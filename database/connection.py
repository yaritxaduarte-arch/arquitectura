"""
database/connection.py
-----------------------
Aquí vive TODO lo relacionado con la conexión a la base de datos.

Responsabilidad de este archivo (y solo esta):
- Crear el "engine" de SQLAlchemy (la conexión física a SQLite).
- Crear la fábrica de sesiones (SessionLocal).
- Exponer `Base`, la clase de la que heredarán todos los modelos (tasks/model.py).
- Exponer `get_db`, una función que FastAPI usará como "dependencia" para
  entregarle una sesión de base de datos a cada endpoint y cerrarla al terminar.

Nadie más en el proyecto debería crear su propio engine o su propia sesión:
todos importan desde aquí.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Usamos SQLite. El archivo tasks.db se crea solo, en la raíz del proyecto,
# la primera vez que se ejecuta la app (y está en .gitignore).
DATABASE_URL = "sqlite:///./tasks.db"

# check_same_thread=False es necesario porque SQLite por defecto solo permite
# un hilo, y Uvicorn/FastAPI pueden manejar peticiones en hilos distintos.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# SessionLocal es una "fábrica" de sesiones. Cada request de la API pedirá
# una sesión nueva a través de get_db().
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es la clase de la que van a heredar los modelos (ver tasks/model.py).
Base = declarative_base()


def get_db():
    """
    Dependencia de FastAPI: abre una sesión de base de datos, la entrega
    al endpoint que la pida, y la cierra automáticamente al terminar
    (incluso si hubo un error).

    Se usa así en las rutas:

        @router.get("/tasks")
        def listar(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
