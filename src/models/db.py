"""Database connection and session management.

Este módulo configura la conexión a PostgreSQL y proporciona:
- engine: conexión reutilizable a la BD (instanciada una sola vez)
- SessionLocal: factory para crear sesiones de ORM
- get_db(): dependency para usar en FastAPI endpoints
- create_tables(): función para crear todas las tablas al iniciar
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent  # Carpeta 'models'
PROJECT_DIR = BASE_DIR.parent.parent  # Carpeta raíz del proyecto
ENV_PATH = PROJECT_DIR / ".env"

# Carga variables de entorno desde archivo .env
load_dotenv(dotenv_path=ENV_PATH)

# Permite importar 'database' como módulo local desde este archivo
sys.path.insert(0, str(BASE_DIR))

from database import Base  # noqa: E402

# ==================== CONFIGURACIÓN DE CONEXIÓN ====================

# Obtiene la URL de conexión de PostgreSQL desde variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL no está configurado. Define la variable de entorno o usa un archivo .env"
    )

# Crea el motor (engine) de SQLAlchemy
# - echo=False: no muestra logs de SQL (cambiar a True para debug)
# - future=True: usa sintaxis moderna de SQLAlchemy 2.0
# - pool_pre_ping=True: verifica conexión antes de usar (evita conexiones muertas)
engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
)

# SessionLocal: factory que crea nuevas sesiones de ORM
# - autocommit=False: no hace commit automático (control manual)
# - autoflush=False: no hace flush automático (control manual)
# - bind=engine: vincula a nuestro engine
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)


# ==================== FUNCIONES ====================

def get_db():
    """Genera una sesión de base de datos para usar como dependency en FastAPI.
    
    Esta función es un generator que:
    1. Crea una nueva sesión
    2. La entrega al endpoint
    3. La cierra automáticamente al finalizar
    
    Uso en FastAPI:
    ```python
    @app.get("/products")
    def list_products(db: Session = Depends(get_db)):
        return db.query(Product).all()
    ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Crea todas las tablas en PostgreSQL basadas en los modelos SQLAlchemy.
    
    Lee las definiciones en Base.metadata (de database.py) y crea:
    - Tabla 'users' con columnas: id, nombre, email, password_hash, rol
    - Tabla 'products' con columnas: id, nombre, categoria, cantidad, precio, fecha_vencimiento
    
    Si ya existen, no hace nada (no lanza error).
    """
    Base.metadata.create_all(bind=engine)


# ==================== EJECUCIÓN DIRECTA ====================

if __name__ == "__main__":
    # Este código se ejecuta solo si corres el archivo directamente:
    # python src/models/db.py
    create_tables()
    print("✅ Tablas creadas con éxito")
