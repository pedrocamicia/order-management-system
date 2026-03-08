from src.infrastructure.db_config import conectar
from psycopg2.extensions import connection

def get_db():
    db = conectar()
    try:
        yield db
    finally:
        db.close()