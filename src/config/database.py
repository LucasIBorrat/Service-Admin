"""Configuración de la base de datos"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Clase base para todos los modelos"""
    pass


db = SQLAlchemy(model_class=Base)


def run_migrations(app):
    """Ejecuta migraciones necesarias para mantener el schema actualizado"""
    with app.app_context():
        try:
            # Verificar si la columna descripcion existe en clientes
            result = db.session.execute(
                text("PRAGMA table_info(clientes)")
            ).fetchall()
            columns = [row[1] for row in result]
            
            if 'descripcion' not in columns:
                logger.info("Agregando columna 'descripcion' a tabla 'clientes'...")
                db.session.execute(
                    text("ALTER TABLE clientes ADD COLUMN descripcion VARCHAR(255)")
                )
                db.session.commit()
                logger.info("Columna 'descripcion' agregada exitosamente")
        except Exception as e:
            logger.warning(f"No se pudo ejecutar migración: {e}")
            db.session.rollback()


def init_db(app):
    """Inicializa la base de datos con la aplicación Flask"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # Ejecutar migraciones después de crear las tablas
    run_migrations(app)

