"""Configuración centralizada de la aplicación"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


@dataclass
class DatabaseConfig:
    """Configuración de base de datos"""
    url: str
    echo: bool = False


@dataclass
class AppConfig:
    """Configuración general de la aplicación"""
    secret_key: str
    debug: bool
    host: str = '0.0.0.0'
    port: int = 5000


class Settings:
    """
    Configuración centralizada del sistema ServiceAdmin.
    
    Singleton que gestiona toda la configuración de la aplicación.
    """
    _instance: Optional['Settings'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._load_config()
    
    def _load_config(self):
        """Carga la configuración desde variables de entorno"""
        # Configuración de la aplicación
        self.app = AppConfig(
            secret_key=os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production'),
            debug=os.getenv('DEBUG', 'True').lower() == 'true',
            host=os.getenv('HOST', '0.0.0.0'),
            port=int(os.getenv('PORT', 5000))
        )
        
        # Configuración de base de datos
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        instance_dir = os.path.join(base_dir, 'src', 'instance')
        os.makedirs(instance_dir, exist_ok=True)
        db_path = os.path.join(instance_dir, 'serviceadmin.db')
        default_db_url = f'sqlite:///{db_path.replace(os.sep, "/")}'
        
        database_url = os.getenv('DATABASE_URL', default_db_url)
        
        self.database = DatabaseConfig(
            url=database_url,
            echo=os.getenv('DB_ECHO', 'False').lower() == 'true'
        )
    
    @classmethod
    def get_instance(cls) -> 'Settings':
        """Obtiene la instancia única de Settings"""
        return cls()


# Instancia global de configuración
settings = Settings.get_instance()
