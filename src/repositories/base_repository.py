"""Repositorio base con operaciones CRUD genéricas"""
from typing import Generic, TypeVar, List, Optional
from sqlalchemy.orm import Session
from src.config.database import db

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """
    Repositorio base que implementa operaciones CRUD genéricas.
    
    Todas las clases de repositorio específicas deben heredar de esta clase.
    """
    
    def __init__(self, model_class: type[T]):
        """
        Inicializa el repositorio con el modelo de datos.
        
        Args:
            model_class: Clase del modelo SQLAlchemy
        """
        self.model_class = model_class
        self.session: Session = db.session
    
    def create(self, entity: T) -> T:
        """
        Crea una nueva entidad en la base de datos.
        
        Args:
            entity: Entidad a crear
            
        Returns:
            La entidad creada con su ID asignado
        """
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except Exception as e:
            self.session.rollback()
            raise e
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """
        Obtiene una entidad por su ID.
        
        Args:
            entity_id: ID de la entidad
            
        Returns:
            La entidad si existe, None en caso contrario
        """
        return self.session.get(self.model_class, entity_id)
    
    def get_all(self) -> List[T]:
        """
        Obtiene todas las entidades.
        
        Returns:
            Lista de todas las entidades
        """
        return self.session.query(self.model_class).all()
    
    def find_all(self) -> List[T]:
        """Alias para get_all()"""
        return self.get_all()
    
    def update(self, entity: T) -> T:
        """
        Actualiza una entidad existente.
        
        Args:
            entity: Entidad con los datos actualizados
            
        Returns:
            La entidad actualizada
        """
        try:
            self.session.merge(entity)
            self.session.commit()
            return entity
        except Exception as e:
            self.session.rollback()
            raise e
    
    def save(self, entity: T) -> T:
        """
        Guarda una entidad (crea si es nueva, actualiza si existe).
        
        Args:
            entity: Entidad a guardar
            
        Returns:
            La entidad guardada
        """
        try:
            if hasattr(entity, 'codCliente') and entity.codCliente is not None:
                self.session.merge(entity)
            elif hasattr(entity, 'codService') and entity.codService is not None:
                self.session.merge(entity)
            elif hasattr(entity, 'codPresupuesto') and entity.codPresupuesto is not None:
                self.session.merge(entity)
            else:
                self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except Exception as e:
            self.session.rollback()
            raise e
    
    def delete(self, entity_id: int) -> bool:
        """
        Elimina una entidad por su ID.
        
        Args:
            entity_id: ID de la entidad a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existía
        """
        entity = self.get_by_id(entity_id)
        if entity:
            try:
                self.session.delete(entity)
                self.session.commit()
                return True
            except Exception as e:
                self.session.rollback()
                raise e
        return False
    
    def exists(self, entity_id: int) -> bool:
        """
        Verifica si existe una entidad con el ID dado.
        
        Args:
            entity_id: ID a verificar
            
        Returns:
            True si existe, False en caso contrario
        """
        return self.get_by_id(entity_id) is not None
