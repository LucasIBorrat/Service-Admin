"""Repositorio para la entidad Cliente"""
from typing import List, Optional
from src.repositories.base_repository import BaseRepository
from src.models.cliente import Cliente


class ClienteRepository(BaseRepository[Cliente]):
    """Repositorio para operaciones con Clientes"""
    
    def __init__(self):
        super().__init__(Cliente)
    
    def find_by_nombre(self, nombre: str) -> List[Cliente]:
        """
        Busca clientes que contengan el nombre dado.
        
        Args:
            nombre: Nombre a buscar (búsqueda parcial)
            
        Returns:
            Lista de clientes que coinciden
        """
        return self.session.query(Cliente).filter(
            Cliente.nombre.ilike(f'%{nombre}%')
        ).all()
    
    def find_by_email(self, email: str) -> Optional[Cliente]:
        """
        Busca un cliente por su email exacto.
        
        Args:
            email: Email del cliente
            
        Returns:
            El cliente si existe, None en caso contrario
        """
        return self.session.query(Cliente).filter_by(email=email).first()
    
    def find_by_tel(self, tel: str) -> Optional[Cliente]:
        """
        Busca un cliente por su teléfono.
        
        Args:
            tel: Teléfono del cliente
            
        Returns:
            El cliente si existe, None en caso contrario
        """
        return self.session.query(Cliente).filter_by(tel=tel).first()
    
    def get_clientes_con_services_pendientes(self) -> List[Cliente]:
        """
        Obtiene clientes que tienen servicios no entregados.
        
        Returns:
            Lista de clientes con servicios pendientes
        """
        from src.models.service import Service
        return self.session.query(Cliente).join(Service).filter(
            Service.entregado == False
        ).distinct().all()
