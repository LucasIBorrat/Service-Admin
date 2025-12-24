"""Repositorio para la entidad Service"""
from typing import List, Optional
from src.repositories.base_repository import BaseRepository
from src.models.service import Service


class ServiceRepository(BaseRepository[Service]):
    """Repositorio para operaciones con Services"""
    
    def __init__(self):
        super().__init__(Service)
    
    def find_by_cliente(self, cod_cliente: int) -> List[Service]:
        """
        Encuentra todos los servicios de un cliente.
        
        Args:
            cod_cliente: Código del cliente
            
        Returns:
            Lista de servicios del cliente
        """
        return self.session.query(Service).filter_by(
            codCliente=cod_cliente
        ).order_by(Service.fecha.desc()).all()
    
    def find_pendientes(self) -> List[Service]:
        """
        Encuentra servicios que no han sido revisados.
        
        Returns:
            Lista de servicios pendientes de revisión
        """
        return self.session.query(Service).filter_by(
            revisado=False
        ).order_by(Service.fecha).all()
    
    def find_revisados_sin_reparar(self) -> List[Service]:
        """
        Encuentra servicios revisados pero no reparados.
        
        Returns:
            Lista de servicios en proceso
        """
        return self.session.query(Service).filter(
            Service.revisado == True,
            Service.reparado == False
        ).order_by(Service.fecha).all()
    
    def find_reparados_sin_entregar(self) -> List[Service]:
        """
        Encuentra servicios reparados pero no entregados.
        
        Returns:
            Lista de servicios listos para entrega
        """
        return self.session.query(Service).filter(
            Service.reparado == True,
            Service.entregado == False
        ).order_by(Service.fecha).all()
    
    def find_no_entregados(self) -> List[Service]:
        """
        Encuentra todos los servicios que no han sido entregados.
        
        Returns:
            Lista de servicios no entregados
        """
        return self.session.query(Service).filter_by(
            entregado=False
        ).order_by(Service.fecha).all()
    
    def find_by_producto(self, producto: str) -> List[Service]:
        """
        Busca servicios por nombre de producto.
        
        Args:
            producto: Nombre del producto (búsqueda parcial)
            
        Returns:
            Lista de servicios que coinciden
        """
        return self.session.query(Service).filter(
            Service.nomProducto.ilike(f'%{producto}%')
        ).all()
    
    def count_by_estado(self) -> dict:
        """
        Cuenta servicios agrupados por estado.
        
        Returns:
            Diccionario con conteos por estado
        """
        total = self.session.query(Service).count()
        pendientes = self.session.query(Service).filter_by(revisado=False).count()
        revisados = self.session.query(Service).filter(
            Service.revisado == True, Service.reparado == False
        ).count()
        reparados = self.session.query(Service).filter(
            Service.reparado == True, Service.entregado == False
        ).count()
        entregados = self.session.query(Service).filter_by(entregado=True).count()
        
        return {
            'total': total,
            'pendientes': pendientes,
            'revisados': revisados,
            'reparados': reparados,
            'entregados': entregados
        }
